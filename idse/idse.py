import argparse
import re
import pexpect
import sys
import pkg_resources


def load_plugins():
    plugins = []
    for entry_point in pkg_resources.iter_entry_points('idse.plugins'):
        plugin_class = entry_point.load()
        plugins.append(plugin_class())
    return plugins


def clean_text(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def i_donot_speek_english(command: str, key_path: str = None):
    child = pexpect.spawn(command)
    all_outputs = []

    plugins = load_plugins()
    for plugin in plugins:
        if plugin.name() == 'IdseGoogletrans':
            translator = plugin

    while True:
        try:
            # 質問プロンプトが表示されるまでの出力を待ち、取得する
            child.expect(r'.*\)')
            question = child.before.decode('utf-8') + child.after.decode('utf-8')
            all_outputs.append(question)

            # 質問内容を翻訳
            translated_question = translator.translate(clean_text(question))

            # 翻訳された質問を表示
            print('---- origin ----')
            print(question.strip())
            print('---- translate ----')
            print(translated_question.strip())
            print('-----------------')
            user_input = input("input: ")

            child.sendline(user_input)

        except pexpect.exceptions.TIMEOUT:
            continue
        except pexpect.exceptions.EOF:
            break

    # 最終出力を結合して返す
    output = ''.join(all_outputs)
    return output


def config_mode():
    print("Entering configuration mode...")


def main():
    parser = argparse.ArgumentParser(description='Process a command and translate its prompts.')
    parser.add_argument('-c', '--config', action='store_true', help='Enter configuration mode')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='The command to run')

    args = parser.parse_args()

    if args.config:
        config_mode()
        sys.exit(0)
    else:
        if not args.command:
            print("Usage: python script.py <command> | python script.py --config")
            sys.exit(1)

    command = ' '.join(args.command)
    print("Command:", command)

    output = i_donot_speek_english(command)
    print(output)
    

if __name__ == "__main__":
    main()
