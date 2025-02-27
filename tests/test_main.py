import pytest
import os
import sys
import subprocess
import shutil

main_py = ""

@pytest.fixture
def setup_git_environment(tmpdir):
    original_dir = os.getcwd()
    global main_py
    main_py = os.path.join(original_dir, "app/main.py")
    os.chdir(tmpdir)
    yield tmpdir
    os.chdir(original_dir)
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)

def test_init(setup_git_environment):
    print(main_py)
    print(tmpdir)
    result = subprocess.run([sys.executable, main_py, "init"], capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists(".git")
    assert os.path.exists(".git/objects")
    assert os.path.exists(".git/refs")
    assert os.path.exists(".git/HEAD")
    with open(".git/HEAD", "r") as f:
        assert f.read() == "ref: refs/heads/main\n"
    assert "Initialized git directory" in result.stdout

# def test_cat_file(setup_git_environment):
#     subprocess.run([sys.executable, "app/main.py", "init"], capture_output=True, text=True)
#     with open("testfile.txt", "w") as f:
#         f.write("Hello World")
#     subprocess.run([sys.executable, "app/main.py", "hash-object", "-w", "testfile.txt"], capture_output=True, text=True)
#     result = subprocess.run([sys.executable, "app/main.py", "cat-file", "-p", "e59ff97941044f85df5297e1c302d260022b1d1a"], capture_output=True, text=True)
#     assert result.stdout == "Hello World"

# def test_hash_object(setup_git_environment):
#     subprocess.run([sys.executable, "app/main.py", "init"], capture_output=True, text=True)
#     with open("testfile.txt", "w") as f:
#         f.write("Hello World")
#     result = subprocess.run([sys.executable, "app/main.py", "hash-object", "-w", "testfile.txt"], capture_output=True, text=True)
#     assert result.stdout.strip() == "e59ff97941044f85df5297e1c302d260022b1d1a"

# def test_ls_tree(setup_git_environment):
#     subprocess.run([sys.executable, "app/main.py", "init"], capture_output=True, text=True)
#     with open("testfile.txt", "w") as f:
#         f.write("Hello World")
#     subprocess.run([sys.executable, "app/main.py", "hash-object", "-w", "testfile.txt"], capture_output=True, text=True)
#     subprocess.run([sys.executable, "app/main.py", "write-tree"], capture_output=True, text=True)
#     result = subprocess.run([sys.executable, "app/main.py", "ls-tree", "--name-only", "4b825dc642cb6eb9a060e54bf8d69288fbee4904"], capture_output=True, text=True)
#     assert "testfile.txt" in result.stdout

# def test_write_tree(setup_git_environment):
#     subprocess.run([sys.executable, "app/main.py", "init"], capture_output=True, text=True)
#     with open("testfile.txt", "w") as f:
#         f.write("Hello World")
#     subprocess.run([sys.executable, "app/main.py", "hash-object", "-w", "testfile.txt"], capture_output=True, text=True)
#     result = subprocess.run([sys.executable, "app/main.py", "write-tree"], capture_output=True, text=True)
#     assert "Stored tree" in result.stdout
