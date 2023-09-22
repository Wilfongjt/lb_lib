#import settings
#import source.git_commands
#import source.git_script
#import source.project_script
#import source.utility_script
#import source.lb_doc_comments
#import source.lb_recorder
import os
from source.utility_script import UtilityScript
from source.lb_doc_comments import LbDocComments

def main():
    # /docs
    output_folder = os.getcwd().split('/')[0:-1]
    output_folder.append('docs')
    output_folder = '/'.join(output_folder)
    # /source
    input_folder = os.getcwd().split('/')[0:-1]
    input_folder.append('source')
    input_folder = '/'.join(input_folder)

    util = UtilityScript()
    file_list = util.get_file_list(input_folder,'py')

    print('input', input_folder)
    print('output', output_folder)
    #print('list',file_list)
    # source
    input_folder = os.getcwd().split('/')[0:-1]
    input_folder.append('source')
    input_folder = '/'.join(input_folder)
    for f in file_list:
        d = LbDocComments().setFolder(input_folder).setFilename(f).open()
        d.saveAs(output_folder, 'source.{}.md'.format(f))
        print('* {} -> {}'.format(f.ljust(20),'source.{}.md'.format(f)))
    # tests
    input_folder = os.getcwd().split('/')[0:-1]
    input_folder.append('tests')
    input_folder = '/'.join(input_folder)
    file_list = util.get_file_list(input_folder,'py')

    for f in file_list:
        d = LbDocComments().setFolder(input_folder).setFilename(f).open()
        d.saveAs(output_folder, 'tests.{}.md'.format(f))
        print('* {} -> {}'.format(f.ljust(20),'tests.{}.md'.format(f)))

    # scripts
    input_folder = os.getcwd().split('/')[0:-1]
    input_folder.append('scripts')
    input_folder = '/'.join(input_folder)
    file_list = util.get_file_list(input_folder,'sh')

    for f in file_list:
        d = LbDocComments().setFolder(input_folder).setFilename(f).open()
        d.saveAs(output_folder, 'scripts.{}.md'.format(f))
        print('* {} -> {}'.format(f.ljust(20),'scripts.{}.md'.format(f)))

    # bin
    input_folder = os.getcwd().split('/')[0:-1]
    input_folder.append('bin')
    input_folder = '/'.join(input_folder)
    file_list = util.get_file_list(input_folder,'py')

    for f in file_list:
        d = LbDocComments().setFolder(input_folder).setFilename(f).open()
        d.saveAs(output_folder, 'bin.{}.md'.format(f))
        print('* {} -> {}'.format(f.ljust(20),'bin.{}.md'.format(f)))


if __name__ == "__main__":
    # execute as script
    main()