from beginai.exec.embeddings.instructions.parse_and_execute import ParseAndExecute
from freezegun import freeze_time
import json

@freeze_time("2021-05-16")
def test_parse_instructions():
    instructions = json.loads(
        """
            [
                {
                    "user":[
                        {
                            "_chains":[
                            [
                                {
                                    "complexity":1,
                                    "instruct":"Age",
                                    "order":1,
                                    "params":{
                                        
                                    }
                                },
                                {
                                    "complexity":1,
                                    "instruct":"Slice",
                                    "order":2,
                                    "params":{
                                        "maxv":100,
                                        "minv":10,
                                        "num_slices":10
                                    }
                                }
                            ]
                            ],
                            "f_id":"userBirthDate",
                            "higher_order":2
                        },
                        {
                            "complexity":1,
                            "f_id":"userBirthDate",
                            "higher_order":1,
                            "instruct":"Age",
                            "params":{
                            
                            }
                        }
                    ]
                }
            ]
    """
    )

    values = {
        "userbirthdate": "16-05-1991"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse('user')
    assert results == {
        'embedding': [30.0, 4.0],
        'labels': []
    }

def test_parse_instructions_without_matching_id():
    instructions = json.loads("""
        [
            {
                "user":[
                    {
                        "complexity":1,
                        "f_id":"userBirthDate",
                        "higher_order":1,
                        "instruct":"Age",
                        "params":{
                        
                        }
                    }
                ]
            }
        ]
    """)

    values = {
        "userBio": "bio bio"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse('user')
    assert results == {
        'embedding': [0.00011],
        'labels': []
    }

@freeze_time("2021-05-16")
def test_parse_instructions_with_different_camel_case_than_provided():
    instructions = json.loads("""
        [
            {
                "user":[
                    {
                        "complexity":1,
                        "f_id":"USERBIRTHDATE",
                        "higher_order":1,
                        "instruct":"Age",
                        "params":{                        
                        }
                    }
                ]
            }
        ]
    """)

    values = {
        "userbirthdate": "16-05-1991"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse('user')
    assert results == {
        'embedding': [30.0],
        'labels': []
    }

def test_parse_instructions_with_interactions_only():
    instructions = json.loads("""[{
        "interactions": [
                {
                    "instruct": "InteractionEncoding",
                    "complexity": 1,
                    "params": {
                        "sequence_map": { "like": 5, "dislike": 2, "_GB_EMPTY": 0.00011 }
                    },
                    "higher_order": 1,
                    "_with_object": "product"
                },
                {
                    "instruct": "InteractionEncoding",
                    "complexity": 1,
                    "params": {
                        "sequence_map": { "followed": 5, "report": 2, "_GB_EMPTY": 0.00011 }
                    },
                    "higher_order": 2,
                    "_with_object": "user"
                }
            ]
        }]
    """)

    values = { 'product': { '10': ['like' ], '20': ['dislike'] } }
    
    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse('interactions')
    expected = { 
        'product': {
            '10': {
                'sent_bin': 2,
                'sentiment': 5,
                'label': "POSITIVE"
            }, 
            '20': {
                'sent_bin': 1,
                'sentiment': 2,
                'label': "NEGATIVE"
            }
        } 
    }
    assert results == expected

def test_parse_instructions_with_interaction_that_doesnt_exist():
    instructions = json.loads("""[{
        "interactions": [
                {
                    "instruct": "InteractionEncoding",
                    "complexity": 1,
                    "params": {
                        "sequence_map": { "like": 5, "dislike": 2, "_GB_EMPTY": 0.00011 }
                    },
                    "higher_order": 1,
                    "_with_object": "product"
                },
                {
                    "instruct": "InteractionEncoding",
                    "complexity": 1,
                    "params": {
                        "sequence_map": { "followed": 5, "report": 2, "_GB_EMPTY": 0.00011 }
                    },
                    "higher_order": 2,
                    "_with_object": "user"
                }
            ]
        }]
    """)

    values = { 'differentobject': { '10': ['like' ], '20': ['dislike'] }, 'product': {'10': ['like']} }
    
    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse('interactions')
    expected = {
        'differentobject': {}, 
        'product': {
            '10': {
                'sent_bin': 2,
                'sentiment': 5,
                'label': "POSITIVE"
            }
        }
    }
    assert results == expected


def test_parse_labels_that_exists():
    instructions = json.loads("""[        
        {   
            "user": {

            },
            "labels":{
                "user":[
                    "fake",
                    "not_fake",
                    "something"
                ],
                "product":[
                    "fruit",
                    "shirt"
                ],
                "message":[
                    "something"
                ]
            }
        }
    ] """)

    values = { 
        "user": {
            "labels": ['fake', "not_fake"]
        }
    }
    
    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values.get('user'))
    results = parse_and_execute.parse('user')
    expected = {
        "embedding": [],
        "labels": ['fake', "not_fake"]
    }
    assert sorted(results) == sorted(expected)

def test_parse_labels_that_dont_exist():
    instructions = json.loads("""[        
        {   
            "product": {

            },
            "labels":{
                "product":[
                    "fruit",
                    "shirt"
                ]
            }
        }
    ] """)

    values = { 
        "product": {
            "labels": ['fake']
        }
    }
    
    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values.get('product'))
    results = parse_and_execute.parse('product')
    expected = {
        "embedding": [],
        "labels": []
    }
    assert sorted(results) == sorted(expected)

def test_boolean_values():
    instructions = json.loads(""" [{
        "home":[
            {
                "instruct":"Boolean",
                "complexity":1,
                "params":{
                    "true":2,
                    "false":1,
                    "_GB_EMPTY": 0.00011
                },
                "f_id":"has_hottub",
                "higher_order":1
        },
        {
                "instruct":"Boolean",
                "complexity":1,
                "params":{
                    "true":2,
                    "false":1,
                    "_GB_EMPTY": 0.00011
                },
                "f_id":"has_true",
                "higher_order":1
        }
        ]
    }] """)

    values = { 
        "has_hottub": 0,
        "has_true": 1
    }
    
    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse('home')
    expected = {
        "embedding": [1.0, 2.0],
        "labels": []
    }
    assert sorted(results) == sorted(expected)