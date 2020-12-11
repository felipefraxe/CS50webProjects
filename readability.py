from cs50 import get_string

def main():
    text = get_string("text: ")
    cl = count_letters(text)
    cw = count_words(text)
    cs = count_sentences(text)
    
    l = (cl / cw) * 100
    s = (cs / cw) * 100
    
    index = round((0.0588 * l) - (0.296 * s) - 15.8)
    
    if index < 1:
        print("Before grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")
        
def count_letters(txt):
    c = 0
    for i in txt:
        if i.isalpha():
            c += 1
    return c
    
def count_words(txt):
    c = 1
    for i in txt:
        if i.isspace():
            c += 1
    return c
    
def count_sentences(txt):
    c = 0
    for i in txt:
        if i == "." or i == "?" or i == "!":
            c += 1
    return c
    
main()