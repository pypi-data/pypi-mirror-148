from beginai.exec.embeddings.instructions.text import Length, CountDigits, StandardName

def test_text_length():
    value = 'My string'    
    assert len(value) == Length().apply(value)

def test_counting_number_of_digits_should_be_zero():
    value = 'No digits here'
    expected = 0
    assert expected == CountDigits().apply(value)

def test_counting_number_of_digits_should_be_two():
    value = '1 digit here and another 1 here'
    expected = 2
    assert expected == CountDigits().apply(value)

def test_name_standard_even_when_maskered():
    standard_names = ['Chandler', 'Ross', 'Joey', 'Rachel', 'Phoebe', 'Monica']
    masked_name = 'Ch?an(dl)er'
    expected = True
    assert expected == StandardName(standard_names).apply(masked_name)