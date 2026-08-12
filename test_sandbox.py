import os
import subprocess

os.makedirs('/var/elab-sandbox/test2', exist_ok=True)
with open('/var/elab-sandbox/test2/main.c', 'w') as f:
    f.write('int main(){return 0;}')

r = subprocess.run([
    'docker', 'run', '--rm', 
    '-v', '/var/elab-sandbox/test2:/box:rw', 
    'elab-sandbox', 'sh', '-c', 
    'cd /box && gcc main.c -o program && ls -la && ./program'
], capture_output=True, text=True)

print('OUT:', r.stdout)
print('ERR:', r.stderr)
print('CODE:', r.returncode)
