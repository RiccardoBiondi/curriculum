#!/usr/bin/env python
# -*- coding: utf-8 -*-

from habanero import Crossref
from scholarly import scholarly
from abc import ABC, abstractmethod
from typing import NoReturn, List, Tuple, Dict, Optional, IO, Any

AUTHOR_NAME = 'Riccardo'
AUTHOR_SURNAME = 'Biondi'
AUTHOR_SCHOLAR_ID = 'EfruuU4AAAAJ'
OUTPUT_FILENAME = 'my_publication_list.bib'
OPTIONAL_FIELDS = ['ISSN', 'publisher', 'page', 'volume', 'url']

def get_bibtex_list_from_publication_title(publication_title: str) -> List[Dict[str, str]]:
    '''
    '''

    cr = Crossref()
    result = cr.works(query=publication_title)
    res = result['message']['items']

    return res

def _get_valid_bibtex_entrance(entrance: Any):

    if isinstance(entrance, list) | isinstance(entrance, tuple):
        return entrance[0]
    
    return entrance

class UserGoogleScholarPublicationList:

    def __init__(self, author_name: str, author_surname: str, author_id: Optional[str] = None) -> None:
        '''
        '''

        self.author_name = author_name
        self.author_surname = author_surname
        self.author_id = author_id
        
        self.publication_list = {}
        
    def query(self) -> None:
        '''
        '''
        search_query = scholarly.search_author(' '.join((self.author_name, self.author_surname)))
        author = next(search_query)
        if self.author_id is not None:
            count = 0 # counter to avoid infinite loop
            while (self.author_id != author['scholar_id']) & (count < 100):
                count = count + 1
                author = next(search_query)
        
        author = scholarly.fill(author)
        
        self.publication_list =  [pub['bib']['title'] for pub in author['publications']]

class FilterBibTexListBy(ABC):

    @abstractmethod
    def __init__(self) -> None:
        '''
        '''
        self.valid_bibtex_list = []
        raise  NotImplementedError()
    
    @abstractmethod
    def setBibTexListToParse(self, bibtex_list: List[Dict[str, str]]) -> None:
        '''
        '''
        raise NotImplementedError()

    @abstractmethod
    def filter(self) -> None:
        '''
        '''
        raise NotImplementedError() 


class FilterBibTexListByAythor(FilterBibTexListBy):
    
    def __init__(self, author_name: Tuple[str]) -> None:
        '''
        '''

        self.bibtex_list = []
        self.author_name = author_name
        self.valid_bibtex_list = []

    def setBibTexListToParse(self, bibtex_list: List[Dict[str, str]]) -> None:

        self.bibtex_list = bibtex_list
    
    def filter(self) -> None:

        self.valid_bibtex_list  = [x for x in self.bibtex_list if self._isPublicationValid(x)]
        

    def _isPublicationValid(self, publication_bibtex: Dict[str, str]) -> bool:
        '''
        '''
        try:
            publication_authors = ' and '.join([', '.join([i['family'],
                                         i['given']])
                              for i in publication_bibtex['author']])
            return (self.author_name[1] in publication_authors) & (self.author_name[0] in publication_authors)
        except KeyError:
            # bacause 'family' and 'given' are mandatory fields.
            # If they do not exists, then the publication bibtex is not valid
            return False

        
class WriteBibtexFromDict:
    '''
    '''

    def __init__(self, bibtex_dict: Dict[str, str], optional_fields: List[str] = []) -> None:

        self.bibtex_dict = bibtex_dict
        self.optional_fields = optional_fields

    def _make_mandatory_fields_string(self) -> str:
        '''
        '''

        authors = ' and '.join([', '.join([i['family'],
                                         i['given']])
                              for i in self.bibtex_dict['author']])
        
        title = self.bibtex_dict['title'][0]
        journal = self.bibtex_dict['container-title'][0]
        doi = self.bibtex_dict['DOI']

        mandatory_str = f'{doi},\n author={{{authors}}},\n title={{{title}}},\n journal={{{journal}}},\n doi={{{doi}}},\n'
        
        return mandatory_str
    def _make_optional_fields_str(self) -> str:
        '''
        '''

        args_list = [
            f' {field}={{{_get_valid_bibtex_entrance(self.bibtex_dict[field])}}}' for field in self.optional_fields if field in self.bibtex_dict
        ]

        return ',\n'.join(args_list)
    
    def _make_date_str(self) -> str:
        '''
        '''

        try:
            year, month, *day = x['published']['date-parts'][0]

            date_str = f' year={{{year}}},\n month={{{month}}}'


            if day:
                date_str.join(f',\n day="{day}"')
            return date_str
        except:
            return ''


    def write(self, output_stream: IO) -> None:
        
        _ = output_stream.write('@article{')
        _ = output_stream.write(self._make_mandatory_fields_string())
        _ = output_stream.write(self._make_optional_fields_str())
        _ = output_stream.write(self._make_date_str())
        _ = output_stream.write('\n}\n\n')

def main() -> None:

    # Retrieve the author specific publication titles from google scholar
    me = UserGoogleScholarPublicationList(AUTHOR_NAME, AUTHOR_SURNAME, AUTHOR_SCHOLAR_ID)
    _ = me.query()

    print(f'Found {len(me.publication_list)} publications for {AUTHOR_NAME} {AUTHOR_SURNAME}')

    # Instantiate some helper class to filter the publications bibtex
    bibtex_filter = FilterBibTexListByAythor((AUTHOR_NAME, AUTHOR_SURNAME))

    # Now, for each publication title
    with open(OUTPUT_FILENAME, 'w') as fp:

        for publication_title in me.publication_list:
            print(f"Filtering {publication_title}")
            publication_bibtex_list = get_bibtex_list_from_publication_title(publication_title)
            _ = bibtex_filter.setBibTexListToParse(publication_bibtex_list)
            _ = bibtex_filter.filter()
        
            if len(bibtex_filter.valid_bibtex_list) > 0:
            
                writer = WriteBibtexFromDict(bibtex_filter.valid_bibtex_list[0], OPTIONAL_FIELDS)
                _ = writer.write(fp)

            else:
                print(f"No valid bibtex found")



if __name__ == '__main__':
    main()
