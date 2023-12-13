"""Calculate relationships between people in a family."""


from argparse import ArgumentParser
import json
from relationships import relationships
import sys


class Person:
    """A person in a family.
    
    Attributes:
        name (str): the person's name.
        gender (str): the person's gender ('m', 'f', or 'n').
        parents (list of Person): the person's parents.
        spouse (Person): the person's spouse.
    """
    def __init__(self, name, gender):
        """Initialize a new Person.
        
        Args:
            name (str): the person's name.
            gender (str): the person's gender ('m', 'f', or 'n').
        
        Side effects:
            Creates attributes name, gender, parents, and spouse.
        """
        self.name = name
        self.gender = gender
        self.parents = []
        self.spouse = None
    
    def add_parent(self, parent):
        """Adds a parent to the parents attribute."""
        self.parents.append(parent)
    
    def set_spouse(self, spouse):
        """Sets the spouse attribute."""
        self.spouse = spouse
    
    def connections(self):
        """Identify potential lowest common relatives and what the connection
        to each of these people is.
        
        Connections will be expressed as sequences of P and S where P represents
        a parent relationship and S represents a spouse relationship. For
        example, the connection to a person's grandparent is "PP"; the
        connection to a person's parent-in-law is "SP". The sequence
        representing the person themselves is an empty string (""). We will call
        these sequences "paths".
        
        Returns:
            dict of {Person: str}: keys are potential lowest common relatives
            and values are the path from self to that relative, as described
            above.
        """
        conn = {self: ""}
        queue = [self]
        while queue:
            person = queue.pop(0)
            path = conn[person]
            for parent in person.parents:
                if parent not in conn:
                    conn[parent] = path + "P"
                    queue.append(parent)
            if ("S" not in path and person.spouse is not None
                    and person.spouse not in conn):
                conn[person.spouse] = path + "S"
                queue.append(person.spouse)
        return conn
    
    def relation_to(self, other):
        """Determine self's relationship to other.
        
        Args:
            other (Person): another Person object.
        
        Returns:
            str or None: `None` if `self` and `other` are not related, or the
            term that describes `self`'s relationship to `other`. The returned 
            string is a term that could complete the following sentence: "`self`
            is `other`'s _____." The catch-all term "distant relative" will be
            used when no more specific term is available.
        """
        myconn = self.connections()
        otherconn = other.connections()
        shared = set(myconn) & set(otherconn)
        if not shared:
            return None
        lcr = min(shared, key=lambda p: len(f"{myconn[p]}:{otherconn[p]}"))
        path = f"{myconn[lcr]}:{otherconn[lcr]}"
        return (relationships[path][self.gender]
                if path in relationships
                else "distant relative")


class Family:
    """A family.
    
    Attributes:
        people (dict of str: Person): people in the family. The keys are names
            and the values are Person objects.
    """
    def __init__(self, familydata):
        """Build a family structure and keep track of the people in it.
        
        Args:
            familydata (dict): a dictionary with the following keys:
                "individuals": a dictionary where each key is the name of a
                    person in the family and each value is that person's gender
                    ('m', 'f', or 'n').
                "parents": a dictionary where each key is the name of a person
                    in the family and each value is a list of the names of that
                    person's parents.
                "couples": a list of lists; each inner list contains two names.
                    These two people are married to each other.
        
        Side effects:
            Populates people attribute.
        """
        self.people = dict()
        for name, gender in familydata["individuals"].items():
            self.people[name] = Person(name, gender)
        for name, parents in familydata["parents"].items():
            for parent in parents:
                self.people[name].add_parent(self.people[parent])
        for name1, name2 in familydata["couples"]:
            self.people[name1].spouse = self.people[name2]
            self.people[name2].spouse = self.people[name1]
    
    def relation(self, name1, name2):
        """Determine the relationship of two people in the family.
        
        The relationship will be expressed in terms of `name1` (name1 is name2's
        _____).
        
        Args:
            name1 (str): the name of the first person.
            name2 (str): the name of the second person.
            
        Returns:
            str or None: `None` if `name1` and `name2` are not related, or the
            term that describe's `name1`'s relationship to `name2`. The returned
            string is a term that could complete the following sentence:
            "`name1` is `name2`'s _____." The catch-all term "distant relative"
            will be used when no more specific term is available.
        """
        person1 = self.people[name1]
        person2 = self.people[name2]
        return person1.relation_to(person2)


def main(filepath, name1, name2):
    """Read family data, build a family structure, and determine the relationship
    between name1 and name2.
    
    Args:
        filepath (str): path to a JSON file containing an object with properties
            "individuals", "parents", and "couples", as described by the
            `Family.__init__()` docstring.
        name1 (str): the name of the first person.
        name2 (str): the name of the second person.
    
    Side effects:
        Writes to stdout.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        familydata = json.load(f)
    family = Family(familydata)
    rel = family.relation(name1, name2)
    if rel is None:
        print(f"{name1} is not related to {name2}")
    else:
        print(f"{name1} is {name2}'s {rel}")


def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects three command-line arguments: the path to a JSON file containing
    family data, the name of a person in the file about whom a relationship term
    is needed, and the name of another person in the file whose relationship to
    the first person is to be determined.
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        argparse.Namespace: a namespace object with properties "filepath"
            (path to a JSON file containing family data), "name1" (the name of
            a person in the family described by `filepath`), and "name2" (the
            name of a second person in the family.)            
    """
    parser = ArgumentParser()
    parser.add_argument("filepath", help="path to family data in JSON format")
    parser.add_argument("name1", help="determine who this person is in relation"
                        " to name2")
    parser.add_argument("name2", help="determine who name1 is in relation to"
                        " this person")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filepath, args.name1, args.name2)
