
import os
from source.utility_script import UtilityScript
from source.lb_doc_comments import LbDocComments

def main():

    # /docs
    output_folder = os.getcwd().split('/')[0:-1]
    output_folder.append('docs')
    output_folder = '/'.join(output_folder)

    util = UtilityScript()

    print('output', output_folder)

    root_folder = os.getcwd().split('/')[0:-1]
    bin_folder = os.getcwd().split('/')[0:-1]
    bin_folder.append('bin')
    scripts_folder = os.getcwd().split('/')[0:-1]
    scripts_folder.append('scripts')
    source_folder = os.getcwd().split('/')[0:-1]
    source_folder.append('source')
    tests_folder = os.getcwd().split('/')[0:-1]
    tests_folder.append('tests')
    # on line per file ext and folder
    input_folders = [
        {'folder': '/'.join(root_folder), 'ext': 'env', 'out_tmpl':'{}.md'},
        {'folder': '/'.join(root_folder), 'ext': 'py', 'out_tmpl': 'bin.{}.md'},
        {'folder':'/'.join(bin_folder), 'ext': 'py','out_tmpl': 'bin.{}.md'},
        {'folder':'/'.join(scripts_folder), 'ext': 'sh', 'out_tmpl': 'scripts.{}.md'},
        {'folder':'/'.join(source_folder), 'ext': 'py','out_tmpl': 'source.{}.md'},
        {'folder':'/'.join(tests_folder), 'ext': 'py','out_tmpl': 'tests.{}.md'}
    ]

    for input_folder in input_folders:
        #print('folder', input_folder['folder'])
        input_files = util.get_file_list(input_folder['folder'],input_folder['ext'])
        for f in input_files:
            d = LbDocComments().setFolder(input_folder['folder']).setFilename(f).open()
            d.saveAs(output_folder, input_folder['out_tmpl'].format(f))
            print('* {} -> {}'.format(f.ljust(20), input_folder['out_tmpl'].format(f)))

if __name__ == "__main__":
    # execute as script
    main()