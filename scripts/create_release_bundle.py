"""Copyright (c) 2005-2024, University of Oxford.
All rights reserved.

University of Oxford means the Chancellor, Masters and Scholars of the
University of Oxford, having an administrative office at Wellington
Square, Oxford OX1 2JD, UK.

This file is part of Chaste.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * Neither the name of the University of Oxford nor the names of its
   contributors may be used to endorse or promote products derived from this
   software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from pathlib import Path

import shutil

VERSION_STRING = '2024.2'

CONTENT_DIR = Path(__file__).parent.parent / 'site' / 'content'
DOCS_DIR = CONTENT_DIR / 'docs'
RELEASES_DIR = CONTENT_DIR / 'releases'
NEW_RELEASE_DIR = RELEASES_DIR / VERSION_STRING

def create_new_release_dir(exists_ok: bool = False) -> None:
    NEW_RELEASE_DIR.mkdir(parents=True, exist_ok=exists_ok)

def get_frontmatter_entry() -> str:
    return f'version: "{VERSION_STRING}"'

def insert_frontmatter() -> None:
    md_files = NEW_RELEASE_DIR.glob('**/*.md')

    for file in md_files:
        with open(file, 'r') as f:
            content = f.read()
        with open(file, 'w') as f:
            f.write(content.replace('\n---', f'\n{get_frontmatter_entry()}\n---', 1))


def is_valid_version_number() -> bool:
    """
    Validates if the given string s matches the format number.number.
    Returns True if the format is correct, False otherwise.
    """
    parts = VERSION_STRING.split('.')
    if len(parts) != 2:
        return False

    return all(part.isdigit() for part in parts)


def copy_files():
    assert DOCS_DIR.is_dir()
    copy_directory(DOCS_DIR, NEW_RELEASE_DIR)
    


def copy_directory(source, destination):
    """
    Copy the entire directory tree at 'source' to the new location 'destination'.
    """
    try:
        shutil.copytree(source, destination)
        print(f"Directory copied from {source} to {destination}")
    except Exception as e:
        print(f"Error occurred while copying the directory: {e}")


if __name__ == '__main__':
   
    if not is_valid_version_number():
        print('Invalid version number. Should be e.g. "2024.1"')
        exit(1)
    
    copy_files()
    insert_frontmatter()
