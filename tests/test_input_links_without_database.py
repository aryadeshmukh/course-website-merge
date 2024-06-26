from typing import List
import pytest

open('../course-links.txt', 'w').close()

def handle_new_link(new_link: str) -> None:
    '''
    Adds a new link to be displayed.

    Keyword arguments:
    new_link -- link to be added to the display
    '''
    with open('../course-links.txt', 'a') as file:
        file.write(f'{new_link.strip()}\n')

def delete_link(links: List[str], link_to_delete: int) -> None:
    '''
    Removes link from list of links and link storage.

    Does not execute if link_to_delete is not positive or out of range of links.

    Keyword arguments:
    link_to_delete -- index of link to be deleted (1-indexed)
    '''
    if (link_to_delete <= 0 or link_to_delete > len(links)):
        raise IndexError()
    
    links.pop(link_to_delete - 1)

    # Store links to be kept back into file
    with open('../course-links.txt', 'w') as file:
        for link in links:
            file.write(f'{link}\n')

def list_links() -> List[str]:
    '''Returns a list of all links.'''
    links = []
    with open('../course-links.txt', 'r') as file:
        for link in file:
            link = link.strip()
            if link:
                links.append(link)
    return links

def test_new_link():
    '''Tests adding a new link in the start.'''
    handle_new_link('link1')
    assert list_links() == ['link1']

def test_delete_first_link():
    '''Tests deleting link when there is only one link.'''
    links = list_links()
    delete_link(links, 1)
    assert list_links() == links == []

def test_add_links_after_deletion():
    '''Tests adding links after deleting.'''
    handle_new_link('link1')
    handle_new_link('link2')
    handle_new_link('link3')
    assert list_links() == ['link1', 'link2', 'link3']

def test_delete_middle_link():
    '''Tests deleting links in the middle.'''
    links = list_links()
    delete_link(links, 2)
    assert list_links() == links == ['link1', 'link3']

@pytest.mark.parametrize('test_index', [3, 0, -1])
def test_delete_bad_input(test_index: int):
    '''Tests if delete_link function handles bad input.'''
    links = list_links()
    with pytest.raises(IndexError):
        delete_link(links, test_index)
        