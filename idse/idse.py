import argparse
import os
import re
import sys
import pkg_resources
import urwid
import typing
import tempfile
from contextlib import suppress


def load_plugins():
    plugins = []
    for entry_point in pkg_resources.iter_entry_points('idse.plugins'):
        plugin_class = entry_point.load()
        plugins.append(plugin_class())
    return plugins


def clean_text(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def get_increment(last_text, data):
    common_length = 0
    for i in range(min(len(last_text), len(data))):
        if last_text[i] != data[i]:
            break
        common_length += 1

    increment = data[common_length:]
    return increment


def i_donot_speek_english(command: str, key_path: str = None):
    urwid.set_encoding('utf8')

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    term = urwid.Terminal(['/bin/sh', '-c', f'{command} 2>&1 | tee {temp_file_path}'], encoding='utf-8')

    title_bar_text = urwid.Text(f'{command}', align='left')
    title_bar = urwid.AttrMap(title_bar_text, 'header')

    status_bar_text = urwid.Text('', align='left')
    status_bar = urwid.AttrMap(status_bar_text, 'header')

    idse = urwid.Text(f' -')
    idse_scroll = urwid.BoxAdapter(urwid.ListBox([idse]), height=20)

    mainframe = urwid.Pile(
        [
            ('pack', title_bar),
            (urwid.WEIGHT, 70, term),
            ('pack', status_bar),
            ('pack', idse_scroll),
        ]
    )

    def execute_quit(*args, **kwargs) -> typing.NoReturn:
        raise urwid.ExitMainLoop()

    def input_filter(keys: list[str], raw: list[int]) -> list[str]:
        import time
        nonlocal last_input_time
        last_input_time = time.time()
        return keys

    def handle_resize(widget, size: tuple[int, int]) -> None:
        pass

    def check_for_updates(loop, user_data):
        nonlocal last_mod_time
        nonlocal last_text

        plugins = load_plugins()
        for plugin in plugins:
            if plugin.name() == 'IdseGoogletrans':
                translator = plugin

        status_bar_text.set_text(f'{translator.name()}')

        try:
            current_mod_time = os.path.getmtime(temp_file_path)
            if current_mod_time != last_mod_time:
                with open(temp_file_path, 'r') as f:
                    data = f.read()
                    update_data = get_increment(last_text, data)
                    data_list.append((current_mod_time, update_data))

                update_text = ''
                for i in range(len(data_list)):
                    if data_list[i][0] > last_input_time:
                        update_text += data_list[i][1]

                if update_text:
                    update_text = clean_text(update_text)
                    translated = translator.translate(update_text)
                    idse.set_text(translated)

                last_text = data
                last_mod_time = current_mod_time

        except FileNotFoundError:
            pass

        loop.set_alarm_in(0.02, check_for_updates)

    urwid.connect_signal(term, 'closed', execute_quit)

    with suppress(NameError):
        urwid.connect_signal(term, 'resize', handle_resize)

    try:
        bpm_screen = urwid.display.raw.Screen(bracketed_paste_mode=True)
    except TypeError:
        bpm_screen = urwid.display.raw.Screen()

    palette = [
        ("header", "white", "dark cyan", "bold"),
        ('divider', 'light gray', 'black'),
    ]
    loop = urwid.MainLoop(mainframe, palette, handle_mouse=False, screen=bpm_screen, input_filter=input_filter)

    term.main_loop = loop

    last_mod_time = 0
    last_input_time = 0
    last_text = ''
    data_list = []
    loop.set_alarm_in(0.1, check_for_updates)

    loop.run()

    os.remove(temp_file_path)


def config_mode():
    print('Entering configuration mode...')


def main(is_test=False):
    parser = argparse.ArgumentParser(description='Process a command and translate its prompts.')
    parser.add_argument('-c', '--config', action='store_true', help='Enter configuration mode')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='The command to run')

    args = parser.parse_args()

    if args.config:
        config_mode()
        sys.exit(0)
    else:
        if not args.command:
            print('Usage: python script.py <command> | python script.py --config')
            if is_test:
                args.command = input('Enter a command: ').split()
            else:
                sys.exit(1)

    command = ' '.join(args.command)
    print('Command:', command)

    i_donot_speek_english(command)


if __name__ == '__main__':
    main(is_test=True)
