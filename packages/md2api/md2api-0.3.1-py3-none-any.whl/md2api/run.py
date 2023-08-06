# coding: utf-8
import sys
import json
from pathlib import Path
from typing import NamedTuple, Optional, Iterable
from datetime import datetime

from git import Repo
from markdown import Markdown


class Document(NamedTuple):
    title: str
    heading: str
    path: str
    html_text: str
    published_at: datetime


class Index(NamedTuple):
    title: str
    heading: str
    path: str
    description: str
    published_at: datetime


def parse_markdown_filepaths(path: str) -> Iterable[Path]:
    root = Path(path)
    return root.glob('**/*.md') if root.is_dir() else [root]


def convert_markdown_to_html(text: str) -> str:
    md = Markdown(extensions=['tables', 'fenced_code'])
    return md.convert(text)


def get_lastcommit_date(path: str) -> Optional[datetime]:
    repo = Repo('.')

    try:
        latest_commit = repo.iter_commits('--all', max_count=1, paths=path).__next__()
        latest_committed_date = latest_commit.committed_date
        return datetime.fromtimestamp(latest_committed_date)
    except StopIteration:
        return None


def create_posts(output_path: Path, documents: list[Document]):
    posts_path = output_path / Path('posts')

    for document in documents:
        document_dir_path = posts_path / document.path
        document_dir_path.mkdir(parents=True, exist_ok=True)

        document_path = document_dir_path / Path('index.html')
        document_path.write_text(json.dumps(document._asdict()))


def extract_title(markdown_text: str) -> str:
    title = ''
    for line in markdown_text.splitlines():
        if line.startswith('# '):
            title = line.lstrip('#').strip()
            break

    return title


def extract_description(html_text: str) -> str:
    h1flag = False
    description = ''
    for line in html_text.splitlines():
        if h1flag:
            if line.startswith('<p>'):
                nextp = line.lstrip('<p>').rstrip('</p>')
                if '<' not in nextp and '>' not in nextp:
                    description = nextp
            break

        if line.startswith('<h1>'):
            h1flag = True
    return description


def create_posts_index(output_path: Path, documents: list[Document]):
    index_path = output_path / Path('posts')

    indices: list[Index] = [
        Index(
            title=document.title,
            heading=document.heading,
            path='/' + str(Path('posts') / document.path),
            description=extract_description(document.html_text),
            published_at=document.published_at
        )for document in documents
    ]
    document_path = index_path / Path('index.html')
    document_path.write_text(json.dumps(sorted([index._asdict() for index in indices], key=lambda i: i.get('published_at'))))


def main():
    target_path = Path(sys.argv[1])
    markdown_files = parse_markdown_filepaths(target_path)

    output_path = Path('docs')

    documents = [
        Document(
            title=markdown.stem,
            heading=extract_title(markdown.read_text()),
            path=str(markdown.with_suffix('')),
            html_text=convert_markdown_to_html(markdown.read_text()),
            published_at=get_lastcommit_date(markdown).isoformat()
        ) for markdown in markdown_files if get_lastcommit_date(markdown)
    ]

    create_posts(output_path=output_path, documents=documents)
    create_posts_index(output_path=output_path, documents=documents)


if __name__ == '__main__':
    main()
