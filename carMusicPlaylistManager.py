import os
import argparse
import shutil

from mutagen.easyid3 import EasyID3
import glob


def copy_single_album(path_single_album_source, path_pendrive):
    source_directory_name = [x for x in path_single_album_source.split('/') if x][-1]
    files_paths = glob.glob(os.path.join(path_single_album_source, '*.mp3'))

    destination_directory = os.path.join(path_pendrive, source_directory_name)

    playlist = {}

    no_track_number = 300
    for file_path in files_paths:
        audio = EasyID3(file_path)
        try:
            track_number = int(audio.get('tracknumber')[0])
        except Exception as exc:
            track_number = no_track_number
            no_track_number = no_track_number + 1
        playlist[track_number] = file_path

    if not playlist:
        return
    min_track_number = min(playlist.keys())
    max_track_number = max(playlist.keys())

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for track_number in range(min_track_number, max_track_number + 1):
        selected_file = playlist[track_number]
        file_name = selected_file.split('/')[-1]
        destination = os.path.join(destination_directory, file_name)
        print(f"Copying {selected_file} to {destination}")
        shutil.copy(selected_file, destination)
        print(f"File {selected_file} copied successfuly")


parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help',
)
parser.add_argument('--path-multiple-albums')
parser.add_argument('--path-source')
parser.add_argument('--path-destination', '--path-pendrive', dest='path_pendrive')
args = parser.parse_args()

path_pendrive = args.path_pendrive
if not path_pendrive or not path_pendrive.startswith('/media/'):
    raise RuntimeError("Invalid destination path! Destination path need to be USB drive!")

for files in os.listdir(path_pendrive):
    path = os.path.join(path_pendrive, files)
    try:
        shutil.rmtree(path)
    except OSError:
        os.remove(path)

if args.path_multiple_albums:
    albums_list = [x for x in glob.glob(os.path.join(args.path_multiple_albums, '*')) if os.path.isdir(x)]
    albums_list.sort()

    for path_album in albums_list:
        copy_single_album(
            path_single_album_source=path_album,
            path_pendrive=args.path_pendrive,
        )
elif args.path_source and args.path_pendrive:
    copy_single_album(
        path_single_album_source=args.path_source,
        path_pendrive=args.path_pendrive,
    )
