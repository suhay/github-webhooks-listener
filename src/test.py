from pybars import Compiler

compiler = Compiler()

source = r'tar xzf /project/repo/{{release.sha}}.tar.gz'
template = compiler.compile(source)
print(template({
    'release': {
      'sha': '302f2b072d46b2f48706eb156f162d901be2c088'
      }
}))
