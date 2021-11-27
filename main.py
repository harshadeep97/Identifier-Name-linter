import datetime
from tree_sitter import Language, Parser
import git
import glob
import sys

link=sys.argv[1]
ext=sys.argv[2]
name=sys.argv[3]
out1=sys.argv[4]
out2=sys.argv[5]


Language.build_library(
  # Store the library in the `buid` direry
  'build/my-languages.so',

  # Include one or more languages
  [
    'tree-sitter-go-master',
    'tree-sitter-javascript-master',
    'tree-sitter-python-master',
    'tree-sitter-ruby'
  ]
)

GO_LANGUAGE = Language('build/my-languages.so', 'go')
JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
PY_LANGUAGE = Language('build/my-languages.so', 'python')
RB_LANGUAGE = Language('build/my-languages.so', 'ruby')

py_parser = Parser()
py_parser.set_language(PY_LANGUAGE)

go_parser = Parser()
go_parser.set_language(GO_LANGUAGE)

js_parser = Parser()
js_parser.set_language(JS_LANGUAGE)

rb_parser = Parser()
rb_parser.set_language(RB_LANGUAGE)


dir_name = 'src_code_'+str(datetime.datetime.now())
git.Repo.clone_from(link,dir_name)


py_files=[]
go_files=[]
rb_files=[]
js_files=[]
def walk(root):
    try:
        for i in glob.glob(root+"/*"):
            if i[-3:]=='.py':
                py_files.append(i)
            elif i[-3:]=='.go':
                go_files.append(i)
            elif i[-3:]=='.rb':
                rb_files.append(i)
            elif i[-3:]=='.js':
                js_files.append(i)
            else:
                walk(i)
        return
    except:
        pass
walk('src_code')

def readNodes(parser,src_code):
  nodes_list = []
  def nodes(node):
    if (node.children):
      for node in node.children:
        if (node.type == 'identifier'):
          nodes_list.append(node)
        nodes(node)
    else:
      return
  tree = parser.parse(bytes(src_code, "utf8"))
  root_node = tree.root_node
  nodes(root_node)
  return (nodes_list)

identifiers =''

if ext == '.py' and name=='python':
    for py in py_files:
        with open(py) as f:
            code = f.read()
        nodes_list = readNodes(py_parser,code)
        #Splitting the code
        parameters = []
        for line in code.splitlines():
            parameters.append(line)
        identifiers = identifiers + py + '\n'
        for i in nodes_list:
           line = parameters[i.start_point[0]]
           identifiers = identifiers+'Identifier Name: '+line[i.start_point[1]:i.end_point[1]]\
                         +' Rows: '+str(i.start_point[0])+'-'+str(i.end_point[0])\
                         +' Columns: '+str(i.start_point[1])+'-'+str(i.end_point[1]) +'\n'

elif ext == '.go' and name=='go':
    for go in go_files:
        with open(go) as f:
            code = f.read()
        nodes_list = readNodes(go_parser,code)
        #Splitting the code
        parameters = []
        for line in code.splitlines():
            parameters.append(line)
        identifiers = identifiers + go + '\n'
        for i in nodes_list:
           line = parameters[i.start_point[0]]
           identifiers = identifiers+'Identifier Name: '+line[i.start_point[1]:i.end_point[1]]\
                         +' Rows: '+str(i.start_point[0])+'-'+str(i.end_point[0])\
                         +' Columns: '+str(i.start_point[1])+'-'+str(i.end_point[1]) +'\n'
elif ext == '.js' and name=='javascript':
    for js in js_files:
        with open(js) as f:
            code = f.read()
        nodes_list = readNodes(js_parser,code)
        #Splitting the code
        parameters = []
        for line in code.splitlines():
            parameters.append(line)
        identifiers = identifiers + js + '\n'
        for i in nodes_list:
           line = parameters[i.start_point[0]]
           identifiers = identifiers+'Identifier Name: '+line[i.start_point[1]:i.end_point[1]]\
                         +' Rows: '+str(i.start_point[0])+'-'+str(i.end_point[0])\
                         +' Columns: '+str(i.start_point[1])+'-'+str(i.end_point[1]) +'\n'

if ext == '.rb' and name=='ruby':
    for rb in rb_files:
        with open(rb) as f:
            code = f.read()
        nodes_list = readNodes(rb_parser,code)
        #Splitting the code
        parameters = []
        for line in code.splitlines():
            parameters.append(line)
        identifiers = identifiers + rb + '\n'
        for i in nodes_list:
           line = parameters[i.start_point[0]]
           identifiers = identifiers+'Identifier Name: '+line[i.start_point[1]:i.end_point[1]]\
                         +' Rows: '+str(i.start_point[0])+'-'+str(i.end_point[0])\
                         +' Columns: '+str(i.start_point[1])+'-'+str(i.end_point[1]) +'\n'

text_file = open(out1, "w")
n = text_file.write(identifiers)
text_file.close()



