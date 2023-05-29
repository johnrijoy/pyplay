from player import PlaybackController
from utils import AudioDetails, AudioState
from fetcher import search_song, get_song
from rich import print as rprint
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
)

def welcome_screen():
    rprint("--------------- [bold green]PYPLAY[/bold green] ----------------------")
    rprint()
    rprint("Welcome to Pyplay.\nEnter HELP for list of commands")
    rprint("\nplay song_name \n")
    rprint("to start playing a song")
    rprint("---------------------------------------------")

def help_screen():
    print("play <song_name>   - play song ")
    print("add <song_name>    - to add song to queue")
    print("search <song_name> - display search result")
    print("showq              - to show all songs in the playlist")
    print("nowp               - to show all songs in the playlist")
    print("pause              - pause the song")
    print("stop               - stop the player")
    print("rmlast             - remove last added song")
    print("skip               - skip song")
    print("setvol <0-100>     - enter value between 0 and 100 to set volume")
    print("end , q            - to exit pyplay")

def show_now_playing(audioState : AudioState):

    curr_time = "{:02d}:{:02d}".format(audioState.current_position//60, (audioState.current_position)%60)
    tot_time = "{:02d}:{:02d}".format(audioState.total_duration//60, (audioState.total_duration)%60)


    # Define custom progress bar
    progress_bar = Progress(
        TextColumn("[green] ▶ "),
        BarColumn(),
        TextColumn("[green]{}".format(curr_time)),
        TextColumn("•"),
        TextColumn("[cyan]{}".format(tot_time)),
    )

    # Use custom progress bar
    with progress_bar as p:
        p.console.print("[green]Now Playing")
        p.console.print("[bold red]%40s[/bold red] - [orange1]%s[/orange1]" % (audioState.title[:40], audioState.uploader))
        p.add_task("", completed= audioState.current_position, total=audioState.total_duration)

def process_input(command: str, args: list, playbackController: PlaybackController):

    command = command.lower()

    if command == 'play' or command == 'pl': # and len(inp) != 0:
        if(len(args)<1):
            print("Atleast one argument required")
        else:
            audioDetails = get_song(" ".join(args))
            playbackController.append_song(audioDetails)
        playbackController.start_playback()

    elif command == 'add' or command == 'a':
        if(len(args)<1):
            print("Atleast one argument required")
        else:
            audioDetails = get_song(" ".join(args))
            playbackController.append_song(audioDetails)

    elif command == 'pause' or command == 'resume' or command == 'p':
        playbackController.pause_resume()

    elif command == 'skip' or command == 'sk':
        playbackController.skip_song()

    elif command == 'showq' or command == 'sq':
        song_queue = playbackController.songQ
        print("-- Playlist --")
        for index, song in enumerate(song_queue):
            print("{:3} - {:20} - {}".format(index+1, song.title, song.get_duration()))

    elif command == 'nowp' or command == 'n':
        audio_state = playbackController.get_now_playing()
        show_now_playing(audio_state)

    elif command == 'rmlast' or command == 'rml':
        playbackController.remove_last()

    elif command == 'search' or command == 'sr':
        if(len(args)<1):
            print("Atleast one argument required")
        else:
            audioDetailsList = search_song(" ".join(args))
            for index, song in enumerate(audioDetailsList):
                print("{:3} - {:50} - {}".format(index+1, song.title, song.get_duration()))
            
            print("\nEnter number to select or 0 to go back")
            usr_inp = int(input(">> "))

            if(usr_inp > 0 and usr_inp <= len(audioDetailsList)):
                index = usr_inp-1
                audioDetails = audioDetailsList[index]
                print("adding song to queue: {}".format(audioDetails))
                playbackController.append_song(audioDetails)
            elif(usr_inp>len(audioDetailsList) or usr_inp<0):
                print("number out of range")
            else:
                print("returning ...")

    elif command == 'setvol' or command == 'vl':
        if(len(args)<1):
            print("Atleast one argument required")
        else:
            try:
                new_vol = int(args[0])
                prev_vol = playbackController.set_vol(new_vol)
                if(prev_vol != -1):
                    print("[vol set: {}-->{}]".format(prev_vol, new_vol))
                else:
                    print("Cannot change volume currently")
            except TypeError:
                print("Integer volume required")

    elif command == 'stop' or command == 'st':
        playbackController.stop_playback()

    elif command == 'help' or command == 'h':
        help_screen()

    else:
        print("Enter a valid command. Type HELP for list of available commands")

def get_command() -> tuple:

    raw_user_input = input("-- ")
    split_input = raw_user_input.split(" ")

    if(len(split_input)<1):
        print("No command passed")
        return (None, None)

    command = split_input.pop(0)

    return (command, split_input)


def start_pyplay_cli(playbackController: PlaybackController):

    welcome_screen()

    while True:
        (command, args) = get_command()
        if(command == 'end' or command == 'q'):
            playbackController.end_player()
            break
        else:
            process_input(command, args, playbackController)