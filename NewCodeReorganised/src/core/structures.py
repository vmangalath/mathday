#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core data structures for the Math Day Score Keeper application.

This module contains all non-GUI classes that handle the core functionality
of the program, including school management and competition scoring.
"""

from typing import Dict, List, Optional, Union, Tuple
import csv
import numpy as np
import os
from utils.functions import NextKey, ReplaceTemplate, IsKey


class PreviousSchool:
    """
    Represents a school's historical information from previous competitions.
    
    Attributes:
        name (str): Name of the school
        location (str): Location of the school ('City' or 'Country')
        hist_z_score (float): Historical Z-score from previous competitions
    """
    
    def __init__(self, name: str, location: str, hist_z_score: float) -> None:
        """
        Initialize a PreviousSchool instance.
        
        Args:
            name: Name of the school
            location: Location of the school ('City' or 'Country')
            hist_z_score: Historical Z-score from previous competitions
        """
        self.name = name
        self.location = location
        self.hist_z_score = float(hist_z_score)

    def __str__(self) -> str:
        """Return a string representation of the school."""
        return f"{self.name} ({self.location})"

    def register(self, key: str) -> 'RegisteredSchool':
        """
        Register the school for a competition.
        
        Args:
            key: Unique identifier for the school in the competition
            
        Returns:
            A new RegisteredSchool instance
        """
        return RegisteredSchool(self.name, self.location, self.hist_z_score, key)


class RegisteredSchool(PreviousSchool):
    """
    Represents a school registered for a competition.
    
    Attributes:
        key (str): Unique identifier for the school in the competition
    """
    
    def __init__(self, name: str, location: str, hist_z_score: float, key: str) -> None:
        """
        Initialize a RegisteredSchool instance.
        
        Args:
            name: Name of the school
            location: Location of the school
            hist_z_score: Historical Z-score
            key: Unique identifier for the school in the competition
        """
        super().__init__(name, location, hist_z_score)
        self.key = key

    def __str__(self) -> str:
        """Return a string representation of the registered school."""
        return f"( {self.key} , {self.name} , {self.location} , {self.hist_z_score} )"

    def generate_competition_school(self, 
                                  group_scores: List[int],
                                  swiss_scores: List[int],
                                  cross_scores: List[int],
                                  relay_scores: List[int],
                                  swiss_partners: List[str],
                                  swiss_sites: List[str]) -> 'CompetitionSchool':
        """
        Create a CompetitionSchool instance for this registered school.
        
        Args:
            group_scores: List of scores for the Group Contest
            swiss_scores: List of scores for the Swiss Contest
            cross_scores: List of scores for the Cross Contest
            relay_scores: List of scores for the Relay Contest
            swiss_partners: List of Swiss partners for all rounds
            swiss_sites: List of Swiss sites for all rounds
            
        Returns:
            A new CompetitionSchool instance
        """
        return CompetitionSchool(
            self.key, self.name, self.location, self.hist_z_score,
            group_scores, swiss_scores, cross_scores, relay_scores,
            swiss_partners, swiss_sites
        )


class CompetitionSchool(RegisteredSchool):
    """
    Represents a school during an active competition.
    
    Attributes:
        group_scores (List[int]): Scores for the Group Contest
        swiss_scores (List[int]): Scores for the Swiss Contest
        cross_scores (List[int]): Scores for the Cross Contest
        relay_scores (List[int]): Scores for the Relay Contest
        swiss_partners (List[str]): Swiss partners for all rounds
        swiss_sites (List[str]): Swiss sites for all rounds
        total (int): Current total score of the school
    """
    
    def __init__(self,
                 key: str,
                 name: str,
                 location: str,
                 hist_z_score: float,
                 group_scores: List[int],
                 swiss_scores: List[int],
                 cross_scores: List[int],
                 relay_scores: List[int],
                 swiss_partners: List[str],
                 swiss_sites: List[str]) -> None:
        """
        Initialize a CompetitionSchool instance.
        
        Args:
            key: Unique identifier for the school
            name: Name of the school
            location: Location of the school
            hist_z_score: Historical Z-score
            group_scores: Scores for the Group Contest
            swiss_scores: Scores for the Swiss Contest
            cross_scores: Scores for the Cross Contest
            relay_scores: Scores for the Relay Contest
            swiss_partners: Swiss partners for all rounds
            swiss_sites: Swiss sites for all rounds
        """
        super().__init__(name, location, hist_z_score, key)
        
        self.group_scores = group_scores
        self.swiss_scores = swiss_scores
        self.cross_scores = cross_scores
        self.relay_scores = relay_scores
        
        self.all_score_dict: Dict[str, List[int]] = {
            'Group': self.group_scores,
            'Swiss': self.swiss_scores,
            'Cross': self.cross_scores,
            'Relay': self.relay_scores
        }
        
        self.swiss_partners = swiss_partners
        self.swiss_sites = swiss_sites
        self.total = sum(self.group_scores + self.swiss_scores + 
                        self.cross_scores + self.relay_scores)

    def __str__(self) -> str:
        """Return a string representation of the competition school."""
        return (f"( {self.key} , {self.name} , {self.location} , {self.hist_z_score} , "
                f"{self.group_scores} , {self.swiss_scores} , {self.cross_scores} , "
                f"{self.relay_scores} , {self.swiss_partners} , {self.swiss_sites} )")

    def listify(self) -> List[Union[str, float, int]]:
        """
        Convert the school's data to a flat list.
        
        Returns:
            A list containing all school data in sequence
        """
        return ([self.key, self.name, self.location, self.hist_z_score] +
                self.group_scores + self.swiss_scores + self.cross_scores +
                self.relay_scores + self.swiss_partners + self.swiss_sites)

    def all_zeros_scores(self, contest_name: str) -> bool:
        """
        Check if all scores for a given contest are zero.
        
        Args:
            contest_name: Name of the contest to check
            
        Returns:
            True if all scores are zero, False otherwise
        """
        return all(x == 0 for x in self.all_score_dict[contest_name])

    def total_update(self, contest_string: List[str] = ['A']) -> None:
        """
        Update the total score based on specified contests.
        
        Args:
            contest_string: List of contest identifiers to include in total
                'G' - All Group Questions
                'G1to8' - Group Questions 1 through 8
                'S' - All Swiss Rounds
                'SQ<Number>' - Specific Swiss Round
                'C' - All Cross Questions
                'R' - All Relay Questions
                'A' - All Questions (Overall Total)
        """
        self.total = 0
        
        for contest in contest_string:
            if contest == 'G':
                self.total += sum(self.group_scores)
            elif contest == 'G1to8':
                self.total += sum(self.group_scores[:8])
            elif contest == 'S':
                self.total += sum(self.swiss_scores)
            elif contest.startswith('SQ'):
                round_num = int(contest[2:]) - 1
                if 0 <= round_num < len(self.swiss_scores):
                    self.total += self.swiss_scores[round_num]
            elif contest == 'C':
                # Cross scores are multiplied by 4
                self.total += 4 * sum(self.cross_scores)
            elif contest == 'R':
                self.total += sum(self.relay_scores)
            elif contest == 'A':
                self.total = (sum(self.group_scores) + sum(self.swiss_scores) +
                            4 * sum(self.cross_scores) + sum(self.relay_scores))
                break

    def write_report(self, template_file: str, school_file: str) -> None:
        """
        Generate a report for the school using a template.
        
        Args:
            template_file: Path to the template file
            school_file: Path where the report will be written
        """
        all_output_names = {
            'SchoolName': self.name,
            'SchoolLocation': self.location,
            'SchoolTotal': str(self.total)
        }

        for contest_key, scores in self.all_score_dict.items():
            for i, score in enumerate(scores):
                new_key = f'School{contest_key}Q{i+1}'
                all_output_names[new_key] = str(score)

            new_key = f'School{contest_key}Total'
            if contest_key == 'Cross':
                # Cross final scores are multiplied by 4
                all_output_names[new_key] = str(4 * sum(scores))
            else:
                all_output_names[new_key] = str(sum(scores))

        ReplaceTemplate(template_file, school_file, all_output_names)

    def update_total_score(self) -> None:
        """Update the total score for the school."""
        self.total = (sum(self.group_scores) + sum(self.swiss_scores) +
                     4 * sum(self.cross_scores) + sum(self.relay_scores))

    def update_z_score(self, mean: float, std: float) -> None:
        """
        Update the Z-score for the school.
        
        Args:
            mean: Mean score of all schools
            std: Standard deviation of all scores
        """
        if std == 0:
            self.z_score = 0
        else:
            self.z_score = (self.total - mean) / std

class SwissPair:
    """
    Represents a pair of schools in a Swiss round.
    
    Attributes:
        site (str): The site where the match takes place
        school1_key (str): Key of the first school
        school2_key (str): Key of the second school
    """
    
    def __init__(self, site: str, school1_key: str, school2_key: str) -> None:
        """
        Initialize a SwissPair instance.
        
        Args:
            site: The site where the match takes place
            school1_key: Key of the first school
            school2_key: Key of the second school
        """
        self.site = site
        self.school1_key = school1_key
        self.school2_key = school2_key

    def school_key_in_pair(self, key: str) -> bool:
        """
        Check if a school key is part of this pair.
        
        Args:
            key: The school key to check
            
        Returns:
            True if the key matches either school in the pair
        """
        return (self.school1_key == key) or (self.school2_key == key)

    def __str__(self) -> str:
        """Return a string representation of the Swiss pair."""
        return f"( {self.site} , {self.school1_key} , {self.school2_key} )"


class ListOfSwissPairs:
    """
    Manages a collection of Swiss pairs.
    
    Attributes:
        pairs (List[SwissPair]): List of Swiss pairs
    """
    
    def __init__(self) -> None:
        """Initialize an empty list of Swiss pairs."""
        self.pairs: List[SwissPair] = []

    def add_pair(self, pair: SwissPair) -> None:
        """
        Add a Swiss pair to the list.
        
        Args:
            pair: The Swiss pair to add
        """
        self.pairs.append(pair)

    def get_pairs(self) -> List[SwissPair]:
        """
        Get all Swiss pairs.
        
        Returns:
            List of all Swiss pairs
        """
        return self.pairs

class PreviousSchoolList:
    """
    Manages a list of schools with their historical information.
    
    Attributes:
        school_list (List[PreviousSchool]): List of schools with historical data
        master_file (Optional[str]): Path to the master file containing school data
    """
    
    def __init__(self, school_list: List[PreviousSchool] = None, master_file: Optional[str] = None) -> None:
        """
        Initialize a PreviousSchoolList instance.
        
        Args:
            school_list: Initial list of schools (default: empty list)
            master_file: Path to the master file (default: None)
        """
        self.school_list = school_list or []
        self.master_file = master_file

    def read_from_file(self) -> None:
        """
        Read school data from the master file.
        
        Raises:
            FileNotFoundError: If the master file doesn't exist
        """
        if not self.master_file:
            raise ValueError("No master file specified")

        # Ensure the directory exists
        master_dir = os.path.dirname(self.master_file)
        if not os.path.exists(master_dir):
            os.makedirs(master_dir)

        # Create the file if it doesn't exist and write a header
        if not os.path.exists(self.master_file):
            with open(self.master_file, 'w', newline='') as writefile:
                writer = csv.writer(writefile)
                writer.writerow(['Name', 'Location', 'Historical Z-Score'])

        with open(self.master_file, 'r', newline='') as readfile:
            reader = csv.reader(readfile)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    self.school_list.append(PreviousSchool(row[0], row[1], float(row[2])))

    def write_to_file(self) -> None:
        """
        Write school data to the master file.
        
        Raises:
            ValueError: If no master file is specified
        """
        if not self.master_file:
            raise ValueError("No master file specified")

        # Ensure the directory exists
        master_dir = os.path.dirname(self.master_file)
        if not os.path.exists(master_dir):
            os.makedirs(master_dir)
            
        with open(self.master_file, 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerow(['Name', 'Location', 'Historical Z-Score'])
            for school in self.school_list:
                writer.writerow([str(school.name), str(school.location), str(school.hist_z_score)])

    def add_to_list(self, school: PreviousSchool) -> None:
        """
        Add a school to the list.
        
        Args:
            school: The school to add
        """
        self.school_list.append(school)

    def sort_list(self) -> None:
        """Sort the school list by name."""
        self.school_list.sort(key=lambda school: school.name)

    def print_list(self) -> None:
        """Print all schools in the list."""
        for school in self.school_list:
            print(school)

    def find_name(self, name: str) -> Optional[PreviousSchool]:
        """
        Find a school by name.
        
        Args:
            name: Name of the school to find
            
        Returns:
            The school if found, None otherwise
        """
        for school in self.school_list:
            if school.name == name:
                return school
        return None

    def name_in_list(self, name: str) -> bool:
        """
        Check if a school name exists in the list.
        
        Args:
            name: Name to check
            
        Returns:
            True if the name exists in the list
        """
        return any(school.name == name for school in self.school_list)

class RegisterSchoolList:
    """
    Manages a list of schools registered for a competition.
    
    Attributes:
        school_list (List[RegisteredSchool]): List of registered schools
    """
    
    def __init__(self, school_list: List[RegisteredSchool] = None) -> None:
        """
        Initialize a RegisterSchoolList instance.
        
        Args:
            school_list: Initial list of registered schools (default: empty list)
        """
        self.school_list = school_list or []

    def add_to_list(self, school: RegisteredSchool) -> None:
        """
        Add a school to the registered list.
        
        Args:
            school: The school to add
        """
        self.school_list.append(school)

    def remove_from_list(self, school: RegisteredSchool) -> None:
        """
        Remove a school from the registered list.
        
        Args:
            school: The school to remove
        """
        self.school_list.remove(school)

    def remove_from_list_key(self, key: str) -> None:
        """
        Remove a school from the list by its key.
        
        Args:
            key: The key of the school to remove
        """
        self.school_list = [school for school in self.school_list if school.key != key]

    def sort_list(self) -> None:
        """Sort the school list by name."""
        self.school_list.sort(key=lambda school: school.name)

    def print_list(self) -> None:
        """Print all registered schools."""
        for school in self.school_list:
            print(school)

    def find_key(self, key: str) -> Optional[RegisteredSchool]:
        """
        Find a school by its key.
        
        Args:
            key: The key to search for
            
        Returns:
            The school if found, None otherwise
        """
        for school in self.school_list:
            if school.key == key:
                return school
        return None

    def find_name(self, name: str) -> Optional[RegisteredSchool]:
        """
        Find a school by its name.
        
        Args:
            name: The name to search for
            
        Returns:
            The school if found, None otherwise
        """
        for school in self.school_list:
            if school.name == name:
                return school
        return None

    def key_in_list(self, key: str) -> bool:
        """
        Check if a key exists in the list.
        
        Args:
            key: The key to check
            
        Returns:
            True if the key exists in the list
        """
        return any(school.key == key for school in self.school_list)

    def name_in_list(self, name: str) -> bool:
        """
        Check if a name exists in the list.
        
        Args:
            name: The name to check
            
        Returns:
            True if the name exists in the list
        """
        return any(school.name == name for school in self.school_list)

    def valid_key(self, key: str) -> bool:
        """
        Check if a key is valid.
        
        A valid key consists of a single letter followed by a number.
        
        Args:
            key: The key to validate
            
        Returns:
            True if the key is valid
        """
        return len(key) == 2 and key[0].isalpha() and key[1].isdigit()

    def valid_key_order(self) -> bool:
        """
        Check if all keys in the list are valid.
        
        Returns:
            True if all keys are valid
        """
        return all(self.valid_key(school.key) for school in self.school_list)

class CompetitionSchoolList:
    """
    Manages a list of schools during an active competition.
    
    Attributes:
        school_list (List[CompetitionSchool]): List of schools in the competition
        file (Optional[str]): Path to the competition file
        master_dir (Optional[str]): Path to the master directory
        data_dir (Optional[str]): Path to the data directory
    """
    
    def __init__(self,
                 school_list: List[CompetitionSchool] = None,
                 file: Optional[str] = None,
                 master_dir: Optional[str] = None,
                 data_dir: Optional[str] = None) -> None:
        """
        Initialize a CompetitionSchoolList instance.
        
        Args:
            school_list: Initial list of competition schools (default: empty list)
            file: Path to the competition file (default: None)
            master_dir: Path to the master directory (default: None)
            data_dir: Path to the data directory (default: None)
        """
        self.school_list = school_list or []
        self.file = file
        self.master_dir = master_dir
        self.data_dir = data_dir

    def read_init_files(self) -> None:
        """
        Read initial files for the competition.
        
        This includes reading the competition file and the master file.
        
        Raises:
            FileNotFoundError: If required files don't exist
            ValueError: If required directories are not specified
        """
        if not self.file or not self.master_dir or not self.data_dir:
            raise ValueError("File paths and directories must be specified")
            
        # Implementation details...

    def compete_registered(self, registered_school_list: RegisterSchoolList) -> None:
        """
        Convert registered schools to competition schools.
        
        Args:
            registered_school_list: List of registered schools to convert
        """
        self.school_list = []
        for school in registered_school_list.school_list:
            competition_school = school.generate_competition_school(
                [0] * 10,  # Group scores
                [0] * 5,   # Swiss scores
                [0] * 10,  # Cross scores
                [0] * 5,   # Relay scores
                [''] * 5,  # Swiss partners
                [''] * 5   # Swiss sites
            )
            self.school_list.append(competition_school)

    def sort_list(self) -> None:
        """Sort the school list by name."""
        self.school_list.sort(key=lambda school: school.name)

    def sort_list_name(self) -> None:
        """Sort the school list by name."""
        self.school_list.sort(key=lambda school: school.name)

    def sort_list_scores(self) -> None:
        """Sort the school list by total score in descending order."""
        self.school_list.sort(key=lambda school: school.total, reverse=True)

    def clear_all_swiss(self, round_num: str = '1') -> None:
        """
        Clear all Swiss scores and partners for a specific round.
        
        Args:
            round_num: Round number to clear (default: '1')
        """
        round_index = int(round_num) - 1
        for school in self.school_list:
            school.swiss_scores[round_index] = 0
            school.swiss_partners[round_index] = ''
            school.swiss_sites[round_index] = ''

    def write_to_file(self) -> None:
        """
        Write competition data to file.
        
        Raises:
            ValueError: If no file path is specified
        """
        if not self.file:
            raise ValueError("No file path specified")
            
        with open(self.file, 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            # Write header
            writer.writerow(['Key', 'Name', 'Location', 'HistZScore'] +
                          [f'Group{i+1}' for i in range(10)] +
                          [f'Swiss{i+1}' for i in range(5)] +
                          [f'Cross{i+1}' for i in range(10)] +
                          [f'Relay{i+1}' for i in range(5)] +
                          [f'SwissPartner{i+1}' for i in range(5)] +
                          [f'SwissSite{i+1}' for i in range(5)])
            
            # Write data
            for school in self.school_list:
                writer.writerow(school.listify())

    def read_from_file(self) -> None:
        """
        Read competition data from file.
        
        Raises:
            ValueError: If no file path is specified
            FileNotFoundError: If the file doesn't exist
        """
        if not self.file:
            raise ValueError("No file path specified")
            
        self.school_list = []
        with open(self.file, 'r', newline='') as readfile:
            reader = csv.reader(readfile)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 34:  # Ensure row has all required fields
                    key = row[0]
                    name = row[1]
                    location = row[2]
                    hist_z_score = float(row[3])
                    
                    # Extract scores and other data
                    group_scores = [int(x) for x in row[4:14]]
                    swiss_scores = [int(x) for x in row[14:19]]
                    cross_scores = [int(x) for x in row[19:29]]
                    relay_scores = [int(x) for x in row[29:34]]
                    swiss_partners = row[34:39]
                    swiss_sites = row[39:44]
                    
                    # Create competition school
                    school = CompetitionSchool(
                        key, name, location, hist_z_score,
                        group_scores, swiss_scores, cross_scores, relay_scores,
                        swiss_partners, swiss_sites
                    )
                    self.school_list.append(school)

    def find_key(self, key: str) -> Optional[CompetitionSchool]:
        """
        Find a school by its key.
        
        Args:
            key: The key to search for
            
        Returns:
            The school if found, None otherwise
        """
        for school in self.school_list:
            if school.key == key:
                return school
        return None

    def find_name(self, name: str) -> Optional[CompetitionSchool]:
        """
        Find a school by its name.
        
        Args:
            name: The name to search for
            
        Returns:
            The school if found, None otherwise
        """
        for school in self.school_list:
            if school.name == name:
                return school
        return None

    def key_in_list(self, key: str) -> bool:
        """
        Check if a key exists in the list.
        
        Args:
            key: The key to check
            
        Returns:
            True if the key exists in the list
        """
        return any(school.key == key for school in self.school_list)

    def name_in_list(self, name: str) -> bool:
        """
        Check if a name exists in the list.
        
        Args:
            name: The name to check
            
        Returns:
            True if the name exists in the list
        """
        return any(school.name == name for school in self.school_list)

    def all_zeros_scores(self, key: str, contest_name: str, is_site_key: bool = False, round_num: int = 1) -> bool:
        """
        Check if all scores for a given contest are zero.
        
        Args:
            key: The school key
            contest_name: The name of the contest
            is_site_key: Whether to check the site key
            round_num: The round number
            
        Returns:
            True if all scores are zero, False otherwise
        """
        school = self.find_key(key)
        if school is None:
            return True
        if contest_name == 'Swiss':
            if is_site_key:
                return school.swiss_sites[round_num - 1] == ''
            else:
                return school.swiss_scores[round_num - 1] == 0
        else:
            return school.all_zeros_scores(contest_name)

    def how_many_letters_in_keys(self) -> int:
        """
        Count how many different letters are used in the keys.
        
        Returns:
            The number of different letters in the keys
        """
        letters = set()
        for school in self.school_list:
            letters.add(school.key[0])
        return len(letters)

    def print_list(self) -> None:
        """Print all schools in the list."""
        for school in self.school_list:
            print(school)

    def possible_swiss_sites(self) -> List[str]:
        """
        Get all possible Swiss sites.
        
        Returns:
            A list of all possible Swiss sites
        """
        sites = set()
        for school in self.school_list:
            for site in school.swiss_sites:
                if site != '':
                    sites.add(site)
        return sorted(list(sites))

    def how_many_letters_in_sites(self) -> int:
        """
        Count how many different letters are used in the sites.
        
        Returns:
            The number of different letters in the sites
        """
        letters = set()
        for school in self.school_list:
            for site in school.swiss_sites:
                if site != '':
                    letters.add(site[0])
        return len(letters)

    def update_totals_school(self) -> None:
        """Update total scores for all schools."""
        for school in self.school_list:
            school.total_update()

        # Calculate mean and standard deviation
        scores = [school.total for school in self.school_list]
        mean = np.mean(scores)
        std = np.std(scores)

        # Update Z-scores
        for school in self.school_list:
            school.update_z_score(mean, std)

    def find_swiss_site(self, round_num: str, site: str) -> List[CompetitionSchool]:
        """
        Find schools in a Swiss round at a specific site.
        
        Args:
            round_num: The round number
            site: The site to search for
            
        Returns:
            A list of schools found at the specified site
        """
        schools = []
        for school in self.school_list:
            if school.swiss_sites[int(round_num) - 1] == site:
                schools.append(school)
        return schools

    def find_swiss_site_by_school(self, round_num: str, school_key: str) -> Optional[str]:
        """
        Find the Swiss site for a specific school in a given round.
        
        Args:
            round_num: The round number
            school_key: The key of the school
            
        Returns:
            The site if found, None otherwise
        """
        school = self.find_key(school_key)
        if school is None:
            return None
        return school.swiss_sites[int(round_num) - 1]

    def get_swiss_partners_by_site(self, round_num: str) -> List[Tuple[str, str]]:
        """
        Get all Swiss partners for a given round.
        
        Args:
            round_num: The round number
            
        Returns:
            A list of tuples containing school key and partner
        """
        partners = []
        for school in self.school_list:
            if school.swiss_partners[int(round_num) - 1] != '':
                partners.append((school.key, school.swiss_partners[int(round_num) - 1]))
        return partners

    def print_swiss_partners_csv(self, round_num: str) -> None:
        """
        Print Swiss round pairings to a CSV file.
        
        Args:
            round_num: The round number
        """
        pairs = self.generate_swiss_partners(round_num)
        file_name = f"{self.data_dir}SwissRound{round_num}.csv"

        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['School1', 'School2'])
            for pair in pairs.get_pairs():
                writer.writerow([pair.school1_key, pair.school2_key])

    def print_swiss_partners(self, round_num: str) -> None:
        """
        Print Swiss round pairings to a text file.
        
        Args:
            round_num: The round number
        """
        pairs = self.generate_swiss_partners(round_num)
        file_name = f"{self.data_dir}SwissRound{round_num}.txt"

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"Swiss Round {round_num} Pairings\n")
            f.write("=" * 40 + "\n\n")
            for pair in pairs.get_pairs():
                f.write(f"{pair.school1_key} vs {pair.school2_key}\n")
                f.write(f"{pair.school1_key} vs {pair.school2_key}\n\n")

    def generate_swiss_partners(self, round_num: str) -> ListOfSwissPairs:
        """
        Generate Swiss round pairings.
        
        Args:
            round_num: The round number
            
        Returns:
            A ListOfSwissPairs instance containing the generated pairs
        """
        # Check if previous round scores have been entered
        if int(round_num) > 1:
            for school in self.school_list:
                if school.swiss_scores[int(round_num) - 2] == 0:
                    raise ValueError(f"Scores for round {int(round_num)-1} have not been entered for all schools. Please enter all scores before generating round {round_num}.")

        # Sort schools by total score
        self.school_list.sort(key=lambda x: x.total, reverse=True)

        # Create pairs
        pairs = ListOfSwissPairs()
        used_schools = set()

        for i, school1 in enumerate(self.school_list):
            if school1 in used_schools:
                continue

            # Find the best available opponent
            best_opponent = None
            best_score_diff = float('inf')

            for school2 in self.school_list[i+1:]:
                if school2 in used_schools:
                    continue

                score_diff = abs(school1.total - school2.total)
                if score_diff < best_score_diff:
                    best_opponent = school2
                    best_score_diff = score_diff

            if best_opponent:
                pair = SwissPair(NextKey(self.possible_swiss_sites()), school1.key, best_opponent.key)
                pairs.add_pair(pair)
                used_schools.add(school1)
                used_schools.add(best_opponent)

        return pairs

    def print_final(self) -> None:
        """Print final results to a text file."""
        file_name = f"{self.data_dir}FinalResults.txt"

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("Final Results\n")
            f.write("=" * 40 + "\n\n")

            # Sort by total score
            self.school_list.sort(key=lambda x: x.total, reverse=True)

            for i, school in enumerate(self.school_list, 1):
                f.write(f"{i}. {school.name} ({school.key})\n")
                f.write(f"   Total Score: {school.total}\n")
                f.write(f"   Z-Score: {school.z_score:.3f}\n")
                f.write(f"   Group: {sum(school.group_scores)}\n")
                f.write(f"   Cross: {sum(school.cross_scores)}\n")
                f.write(f"   Relay: {sum(school.relay_scores)}\n")
                f.write(f"   Swiss: {sum(school.swiss_scores)}\n\n")

    def get_top10(self, location: str) -> List[CompetitionSchool]:
        """
        Get top 10 schools for a given location.
        
        Args:
            location: The location to search for
            
        Returns:
            A list of top 10 schools
        """
        self.sort_list_scores()
        top10 = []
        for school in self.school_list:
            if school.location == location:
                top10.append(school)
                if len(top10) == 10:
                    break
        return top10

    def print_overall(self) -> None:
        """Print overall results to a text file."""
        file_name = f"{self.data_dir}OverallResults.txt"

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("Overall Results\n")
            f.write("=" * 40 + "\n\n")

            # Sort by Z-score
            self.school_list.sort(key=lambda x: x.z_score, reverse=True)

            for i, school in enumerate(self.school_list, 1):
                f.write(f"{i}. {school.name} ({school.key})\n")
                f.write(f"   Z-Score: {school.z_score:.3f}\n")
                f.write(f"   Total Score: {school.total}\n\n")

    def update_master_file(self) -> None:
        """Update the master file with results from this competition."""
        master_file = f"{self.master_dir}Schools.csv"
        master_list = PreviousSchoolList(master_file)
        master_list.read_from_file()

        for school in self.school_list:
            master_school = master_list.find_name(school.name)
            if master_school:
                # Update Z-score using weighted average
                master_school.hist_z_score = (master_school.hist_z_score + school.z_score) / 2
            else:
                # Add new school
                master_list.add_to_list(PreviousSchool(school.name, school.location, school.z_score))

        master_list.sort_list()
        master_list.write_to_file() 