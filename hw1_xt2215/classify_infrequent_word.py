#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215"
__date__ = "$Sep 17, 2018"


def classify_infrequent_word_rare(word, word_set):
    if word in word_set:
        return word;
    else:
        return "_RARE_";


def classify_infrequent_word_customized(word, word_set):
    if word in word_set:
        return word;
    else:
        substitute = "_RARE_";
        if is_month(word):
            substitute = "_MONTH_";
        elif is_weekday(word):
            substitute = "_WEEKDAY_";
        elif is_title(word):
            substitute = "_TITLE_";
        elif is_upper(word):
            substitute = "_UPPER_";
        elif is_alpha(word):
            substitute = "_ALPHA_";
        elif is_digit(word):
            substitute = "_DIGIT_";
        elif lower_contains_special(word):
            substitute = "_SPECIAL_";
        return substitute;


def is_month(word):
    months = ("January", "Jan", "February", "Feb", "March", "Mar", "April", "Apr", "May", "June",
              "Jun", "July", "Jul", "August", "Aug", "September", "Sep", "October", "Oct",
              "November", "Nov", "December", "Dec");
    return word.capitalize() in months;


def is_weekday(word):
    weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday");
    return word.capitalize() in weekdays;


def is_upper(word):
    return word.isupper();


def is_title(word):
    return word.istitle();


def is_alpha(word):
    return word.isalpha();


def is_digit(word):
    return word.isdigit();


def lower_contains_special(word):
    specials = (".", ",", "&", "/", ";");
    if word.islower():
        for special in specials:
            if word.__contains__(special):
                return True;
    return False;


def classify_by_standard(word, word_set, standard="RARE"):
    if standard == "RARE":
        return classify_infrequent_word_rare(word, word_set);
    if standard == "CUSTOMIZE":
        return classify_infrequent_word_customized(word, word_set);
