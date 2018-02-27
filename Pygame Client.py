import pygame as pg
import socket               # Import socket module
import os


def main():
    # networking setup
    s = socket.socket()  # Create a socket object
    # host = '127.0.0.1'
    host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    port = 12345  # Reserve a port for your service.

    # set up screen, and rendering options
    font_size = 20

    screen = pg.display.set_mode((400, 800))
    font = pg.font.Font(None, font_size)
    clock = pg.time.Clock()

    color = pg.Color('dodgerblue2')

    # console vars
    user_input_text = ''   # current user input
    console_text_log = []
    console_shutdown = False
    console_shutdown_command = "close"

    # connect to server
    s.setblocking(1)
    s.settimeout(2)
    s.connect((host, port))

    print("CONNECTION ESTABLISHED")
    console_text_log.insert(0,"CONNECTION ESTABLISHED")


    while not console_shutdown:

        # get a message from if possible
        s.settimeout(.1)
        try:
            server_output = s.recv(1024).decode()
            if len(server_output) > 0:
                print('[SERVER] ' + server_output)
                console_text_log.insert(0,'[SERVER] ' + server_output)
            else:
                print("CONNECTION LOST")
                console_text_log.insert(0, "CONNECTION LOST")
                break
        except ConnectionResetError as e:
            print("CONNECTION LOST")
            console_text_log.insert(0, "CONNECTION LOST")
            break
        except Exception as e:
            if str(e) != "timed out":
                print(type(e))

        # Iterate through events, looking for user inputs
        for event in pg.event.get():
            # user hits close window
            if event.type == pg.QUIT:
                return
            # if any key pressed
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # if user presses enter then add text to console log
                    print(user_input_text)
                    console_text_log.insert(0,'[CLIENT] ' + user_input_text)

                    # on command, exit the console and sever connection
                    if user_input_text == console_shutdown_command:
                        console_shutdown = True
                        break

                    # send all commands to server
                    s.send(user_input_text.encode())

                    # reset input text
                    user_input_text = ''

                elif event.key == pg.K_BACKSPACE:
                    user_input_text = user_input_text[:-1]
                else:
                    user_input_text += event.unicode

        # drawing location variables
        console_x = 20
        console_y_increment = 20
        console_y = 20

        # print current user input
        screen.fill((30, 30, 30))
        txt_surface = font.render(":" +user_input_text, True, color)
        screen.blit(txt_surface, (console_x, console_y))

        console_y += console_y_increment

        # print  "console log"  messages below
        for t in console_text_log:
            txt_surface = font.render(t, True, color)
            screen.blit(txt_surface, (console_x, console_y))
            console_y += console_y_increment

        # wipe the display
        pg.display.flip()
        clock.tick(30)




if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()