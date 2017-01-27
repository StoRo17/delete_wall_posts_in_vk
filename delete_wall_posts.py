import time
import webbrowser
import vk_api


APP_ID = 5672498


def captcha_handler(captcha):
    """
        If you have captcha this function is called and it passed the captcha object.
        Via method get_url you can get a link to the image.
        Via method try_again you can send request with captcha code.
    """

    webbrowser.open_new_tab(captcha.get_url())
    key = input("Enter the captcha (it will be open in browser right now): ").strip()

    # Try to send request with captcha again
    return captcha.try_again(key)


def auth(login, password):
    session = vk_api.VkApi(login, password, captcha_handler=captcha_handler,
                           app_id=APP_ID)

    try:
        session.authorization()
        return session
    except vk_api.AuthorizationError as error_msg:
        print("Error: ", error_msg)
        return False


def get_wall_posts(vk_tools, offset):
    wall = vk_tools.get_all('wall.get', 100, {'offset': offset})['items']
    return wall


def delete_wall_posts(vk_tools, vk, offset):
    posts = get_wall_posts(vk_tools, offset)
    for post in posts:
        vk.wall.delete(post_id=post['id'])
        print("Post deleted")


def main():
    while True:
        login = input("Enter your login or phone number: ").strip()
        password = input("Enter your password: ").strip()
        offset = input("Enter the number of offset: ").strip()
        print("\nAuthorization...")
        time.sleep(1)

        vk_session = auth(login, password)
        if vk_session:
            print("Authorization complete successfully")
            time.sleep(0.5)
            print("Cleaning wall...")
            time.sleep(1)

            vk_tools = vk_api.VkTools(vk_session)
            vk = vk_session.get_api()
            delete_wall_posts(vk_tools, vk, offset)
            print("All clean up, goodbye")
            break
        else:
            print("\nTry to enter your credentials again please")

if __name__ == "__main__":
    main()
