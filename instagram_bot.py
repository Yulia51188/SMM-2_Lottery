import requests
import os
import argparse
import instabot
from dotenv import load_dotenv
import re


# def parse_arguments():
#     parser = argparse.ArgumentParser(
#         description='Publish photos from the folder to Instagram'
#     )
#     parser.add_argument(
#         'folder',
#         type=str,
#         help='path to the folder with photos'
#     )        
#     return parser.parse_args()


# def publish_to_instagramm(username, password, folder):
#     bot = instabot.Bot()
#     bot.login(username=username, password=password)
#     if bot.api.last_response.status_code != 200:
#         exit(bot.api.last_response)
#     file_tree = os.walk(folder)
#     image_filenames = []
#     for root, dirs, filenames in file_tree:
#         image_filenames = [os.path.join(root, filename) for filename in filenames]
#     for image_filename in image_filenames:
#         title = os.path.splitext(os.path.basename(image_filename))[0]
#         bot.upload_photo(image_filename, '{0}'.format(title))


def test_instabot(login, password):
    bot = instabot.Bot()
    bot.login(username=login, password=password)
    user_id = bot.get_user_id_from_username("lego")
    user_info = bot.get_user_info(user_id)
    return user_info['biography']


def get_comments_of_post(login, password, post_url):
    bot = instabot.Bot()
    bot.login(username=login, password=password)
    if bot.api.last_response.status_code != 200:
        return bot.api.last_response
    post_id = bot.get_media_id_from_link(post_url)

    # comments = bot.get_media_comments_all(post_id)
    comments = bot.get_media_comments(post_id)        # ONLY FOR DEBUGGING!
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
        # print(f'Friends: {friends} of comment#{index}')
        if len(friends) > 0:
            comments_with_links.append({'comment': comment, 'friends':friends})
    return comments_with_links


def valid_user_names(comments):
    bot = instabot.Bot()
    bot.login(username=login, password=password)
    valid_comment = []
    for comment in comments:
        friends_id = [bot.get_user_id_from_username(username) for username in comment["friends"]]
        if not friends_id is None:
            valid_comment.append(comment)
        print(f'ID друзей: {friends_id}')

    # users_exist = [bool(user_id) for user_id in user_ids]
    # print(f'Логическая сумма: {sum(users_exist)}')
    return 

def main():
    load_dotenv()
    inst_login = os.getenv("INST_LOGIN")
    inst_password = os.getenv("INST_PASSWORD")    
    post_url = "https://www.instagram.com/p/BtON034lPhu/"
    # args = parse_arguments()
    # if not os.path.isdir(args.folder):
    #     exit("The specified directory '{0}' doesn't exist".format(args.folder))
    # publish_to_instagramm(inst_login, inst_password, args.folder)
    # print(test_instabot(inst_login, inst_password))
    
    comments = get_comments_of_post(inst_login, inst_password, post_url)
    filtered_comments = filter_comments_with_link_to_friend(comments)
    participants = [comment["comment"] for comment in filtered_comments if is_users_exist(inst_login, inst_password, comment['friends'])]
    print(f'Участники: {participants}')



if __name__ == '__main__':
    main()

"""
Friends: ['tamella_1', 'solnechny.chelovechek'] of comment#0
Friends: ['marfi_777', 'larisa_altuxova'] of comment#1
Friends: ['ko.m.a.r.i.k', 'gif_glm'] of comment#2
Friends: ['polioli___', 'st.777_'] of comment#3
Friends: ['_vassilek', 'galimjanovakylia'] of comment#4
Friends: ['zameerka', 'happy__olga'] of comment#5
Friends: ['grigorieva88', 'mariiakuzovleva'] of comment#6
Friends: ['moskaleva35', 'marinagrigoreva1501'] of comment#7
Friends: ['daryaostik', 'mariakuzovleva86'] of comment#8
Friends: ['dglush', 'la.risa7158'] of comment#9
Friends: ['grigore3861', 'mariakuzovleva6'] of comment#10
Friends: ['tolstik_kate_13', '_ann_boychuk_'] of comment#11
Friends: ['lovely_sofi_', '_m.lizzie._'] of comment#12
Friends: ['beautybar.rus'] of comment#13
Friends: ['avgkop'] of comment#14
Friends: ['avgkop'] of comment#15
Friends: ['ekaterinavecher'] of comment#1
"""