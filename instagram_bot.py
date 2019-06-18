import requests
import os
import argparse
import instabot
from dotenv import load_dotenv
import re
from pprint import pprint
from time import sleep


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='The script checks if the participants have fulfilled' 
            'the conditions of the competition'
    )
    parser.add_argument(
        'post_url',
        type=str,
        help='URL of Instagram competition post'
    )    
    parser.add_argument(
        'author',
        type=str,
        help='Author of Instagram post'
    )     
    parser.add_argument(
        '-d','--debug_mode',
        action='store_true',
        help='Flag to set debug mode with limit of the comment count 20'
    )     
    return parser.parse_args()

 
def test_instabot(login, password):
    bot = instabot.Bot()
    bot.login(username=login, password=password)
    user_id = bot.get_user_id_from_username("lego")
    user_info = bot.get_user_info(user_id)
    return user_info['biography']


def get_comments_of_post(bot, post_url, debug_mode):
    media_id = bot.get_media_id_from_link(post_url)
    if not bot.api.last_response.status_code == 200:
        raise ValueError(f"The input URL is wrong or post doesn't exist! {bot.api.last_response}")
    if not debug_mode:
        comments = bot.get_media_comments_all(media_id)
    else:
        comments = bot.get_media_comments(media_id)    
    if not bot.api.last_response.status_code == 200:
        raise ValueError(f"The input URL is wrong or post doesn't exist! {bot.api.last_response}")
    return comments


def get_friend_ids(comment):
    regex = re.compile("(?:^|[^\\w])(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|"
        "(?:\\.(?!\\.))){0,28}(?:[A-Za-z0-9_])){0,1})")
    matchArray = regex.findall(comment)
    return matchArray


def filter_comments_with_link_to_friend(comments):
    comments_with_links = []
    for index, comment in enumerate(comments):
        friends = get_friend_ids(comment["text"])
        if len(friends) > 0:
            comments_with_links.append({
                'comment': comment, 
                'friends':friends
            })
    return comments_with_links


def valid_user_names_by_real_friends(bot, comments, debug_mode):
    for index, comment in enumerate(comments):
        if debug_mode:
            print(f'Validate friends {index}')
        friends_ids = [bot.get_user_id_from_username(username) 
                        for username in comment["friends"]]
        sleep(0.5)
        if any(friends_ids):
            comment["username"] = bot.get_username_from_user_id(
                    comment["comment"]["user_id"]
            )
            comment["friend_id"] = friends_ids
            yield comment


def valid_user_names_by_likes(bot, participants, media_url):
    media_id = bot.get_media_id_from_link(media_url)
    likers = bot.get_media_likers(media_id)
    if not bot.api.last_response.status_code == 200 or not likers:
        raise ValidationError(f"Can't get the list of person who liked! "
            "{bot.api.last_response}")
    for  someone in participants:
        if str(someone["comment"]["user_id"]) in likers:
            yield someone


def valid_user_names_by_following(bot, participants, author_username):
    followers = bot.get_user_followers(author_username)
    if not bot.api.last_response.status_code == 200 or not followers:
        raise ValidationError(f"Can't get the list of followers: "
            "{bot.api.last_response}")    
    for  someone in participants:
        if str(someone["comment"]["user_id"]) in followers:
            yield someone


class AuthError(Exception):
    pass


class ValidationError(Exception):
    pass


def get_winners(inst_login, inst_password, post_url, author_username, 
                    debug_mode):
    bot = instabot.Bot()
    bot.login(username=inst_login, password=inst_password)
    if not bot.api.last_response.status_code == 200:
        raise AuthError(f"Can't authozrize in Instagramm "
            "{bot.api.last_response}")
    try:
        comments = get_comments_of_post(
            bot, 
            post_url, 
            debug_mode
        )
    except ValueError as error:
        raise ValueError(error)
    filtered_comments = filter_comments_with_link_to_friend(comments)
    if not filtered_comments:
        return 
    validation_errors = []
    try:
        comments_with_likes = list(valid_user_names_by_likes(
            bot,
            filtered_comments,
            post_url,
        ))
    except ValidationError as error:
        comments_with_likes = filtered_comments
        validation_errors.append(error)
    try:    
        comments_of_followers = list(valid_user_names_by_following(
            bot,
            comments_with_likes,
            author_username,
        ))
    except ValidationError as error:
        comments_of_followers = comments_with_likes
        validation_errors.append(error)       
    try:        
        comments_with_friends = list(valid_user_names_by_real_friends(
            bot, 
            comments_of_followers,
            debug_mode,
        ))
    except ValidationError as error:
        comments_of_followers = comments_with_likes
        validation_errors.append(error)
    participants_id = [(someone["comment"]["user_id"], someone["username"]) 
                            for someone in comments_with_friends]
    winners = set(participants_id)
    return (winners, validation_errors)


def main():
    load_dotenv()
    inst_login = os.getenv("INST_LOGIN")
    inst_password = os.getenv("INST_PASSWORD")  
    args = parse_arguments()  
    print(f"Debug: {args.debug_mode}")
    print(f'Start fetching comments for {args.post_url}. '
        'It can takes several minutes!')
    try:
        (winners, errors) = get_winners(
            inst_login, 
            inst_password, 
            args.post_url, 
            args.author, 
            args.debug_mode
        )
    except AuthError as error:
        print(f"The script failed due to error occured: {error}")
    except ValueError as error:
        print(f"The script failed to get comments due to error occured: {error}")
    if not winners:
        exit("Sorry, there are no winners found")
    print('Winners:')
    pprint(winners)
    if any(errors):
        print("Some errors occured during proccessing:")
        pprint(errors)


if __name__ == '__main__':
    main()
