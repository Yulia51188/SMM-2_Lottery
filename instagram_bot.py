import requests
import os
import argparse
import instabot
from dotenv import load_dotenv
import re
from pprint import pprint



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


def get_comments_of_post(bot, post_url):
    if bot.api.last_response.status_code != 200:
        return bot.api.last_response
    post_id = bot.get_media_id_from_link(post_url)
    # comments = bot.get_media_comments_all(post_id)  # BASE VERSION
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
        if len(friends) > 0:
            comments_with_links.append({
                'comment': comment, 
                'friends':friends
            })
    return comments_with_links


def valid_user_names_by_real_friends(bot, comments):
    valid_comment = []
    for comment in comments:
        comment["username"] = bot.get_username_from_user_id(
            comment["comment"]["user_id"]
        )
        friends_ids = [bot.get_user_id_from_username(username) 
                        for username in comment["friends"]]
        if any(friends_ids):
            comment["friend_id"] = friends_ids
            valid_comment.append(comment)
    return valid_comment

def valid_user_names_by_likes(bot, participants, media_url):
    media_id = bot.get_media_id_from_link(media_url)
    print(f"Media_id: {media_id}")
    likers = bot.get_media_likers(media_id)
    for  someone in participants:
        if str(someone["comment"]["user_id"]) in likers:
            print(f'Someone {someone["comment"]["user_id"]} in likers')
            yield someone


def main():
    load_dotenv()
    inst_login = os.getenv("INST_LOGIN")
    inst_password = os.getenv("INST_PASSWORD")    
    post_url = "https://www.instagram.com/p/BtON034lPhu/"    
    bot = instabot.Bot()
    bot.login(username=inst_login, password=inst_password)
    comments = get_comments_of_post(bot, post_url)
    filtered_comments = filter_comments_with_link_to_friend(comments)
    participants_with_friends = valid_user_names_by_real_friends(
        bot,
        filtered_comments,
    )
    participants_with_likes = list(valid_user_names_by_likes(
        bot,
        participants_with_friends,
        post_url,
        ))
    participants_id = [(someone["comment"]["user_id"], someone["username"]) 
                        for someone in participants_with_likes]
    pprint(participants_id)


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
Friends: ['ekaterinavecher'] of comment#16
"""

"""
Likers: ['8193766401', '1054396418', '282656770', '1568623622', '3499076614', '7446652937', '180203535', '1632849936', '2990045205', '8956509210', '8174135331', '4399761445', '8136628262', '2910370859', '1368090673', '4366072881', '3948805175', '6518559801', '1730530363', '5558347839', '2269405247', '346432579', '209894469', '4894628941', '6622578772', '1389377624', '795441246', '9911017569', '2867009640', '9302490221', '7585216630', '7408232573', '3096383620', '7922611335', '8675613832', '8545530005', '1641313444', '6125138101', '3825851574', '862075066', '200790204', '5848457404', '1459090628', '8930012357', '1280871621', '2015865031', '1745589454', '195860689', '335340753', '5655318740', '4321427668', '447747288', '5513621720', '7619579101', '1810579683', '4703442149', '4256224487', '8708705512', '5659350249', '4848330987', '2752729341', '5820146942', '1690746124', '8073126158', '4781632794', '6809426206', '1642515743', '3463661857', '1963348263', '1608333609', '5814221100', '7582535982', '7087757623', '1828755772', '6822164797', '5493179716', '3919131975', '6088219975', '6854638922', '3312110925', '7738490203', '7704583518', '7151743329', '3682649445', '1166470503', '1602842988', '176116082', '9043743090', '4212946290', '1818212726', '8664502646', '3244870007', '3938063738', '4052994427', '4748845437', '8012795264', '636823941', '2352054665', '7062685071', '5925260696', '7660823967', '3057085856', '1838130594', '2238298538', '4201713067', '8480031150', '7117535664', '8359652787', '3666241971', '39402932', '7528598970', '8326175165', '8506405312', '623715777', '5749075395', '5892432330', '7914815948', '7696907725', '7945457113', '4465399266', '4977318373', '3271587303', '1486692839', '1579256306', '8553979382', '4116367863', '5520328184', '7075406332', '6697129474', '6847689220', '7561588239', '8736335380', '9609626133', '3999136283', '9384050206', '7215619614', '8468391469', '3263231534', '4708635195', '6139883068', '4649981503', '6913053254', '6997916230', '670177867', '6919756370', '1186092630', '5561071196', '4208564834', '5922612835', '28590694', '5747372653', '3971125870', '5573252720', '5485351536', '1552986741', '1912630901', '5825733238', '7998503541', '773451398', '1548757645', '4680811150', '556306064', '4586223248', '3267975825', '3277661844', '7461469849', '2941355673', '7298212507', '6358124190', '2116002463', '196427430', '6860597926', '10705792690', '6166278836', '4341054135', '573009592', '1707885252', '4643524292', '5732660935', '2282909386', '368231118', '8890446549', '9136605911', '2138848985', '4470665950', '5468903137', '695599842', '695187176', '10216216311', '4111074046', '8253226752', '4701830916', '10604375813', '2310895367', '5770047241', '4929311498', '4486971158', '38755096', '5491989276', '8580955934', '5471493918', '5418664737', '1454260005', '2056009510', '2266561319', '7189536554', '8521377578', '7390115629', '4718642990', '7650058042', '8636606267', '8165929791', '543962953', '4490796874', '3868799819', '1078785872', '1222811473', '7210113876', '1008676696', '3296530266', '9062180700', '1242302303', '6391728992', '7465962344', '6905334634', '4701315947', '4013113199', '4098311025', '6047185780', '3160671096', '7747074938', '656947067', '7183764350', '3236595586', '6159148931', '8342338447', '2150577040', '5555414930', '1104029598', '10019802017', '1340329890', '6969772962', '3065881509', '4363113383', '1204303787', '3473014706', '8459543475', '1401921462', '5717450678', '7498176446', '1475044286', '4532332490', '1400299471', '5565828055', '8419046359', '1048664028', '9130282972', '460978145', '3730118631', '1686983669', '4784934909']

"""