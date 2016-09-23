from nlgen.cfg import (
    CFG,
    read_production,
    read_cfg,
    Production, ProductionRef,
    ProductionUnion,
    Terminal
)


def test_simple_case():
    result = read_production("PRONOUN VI NOUN")
    assert result == Production([
        ProductionRef("PRONOUN"),
        ProductionRef("VI"),
        ProductionRef("NOUN"),
    ])

CFG_EXAMPLE = """
SENTENCE -> PRONOUN VERB NOUN;
PRONOUN -> "I" {"person": "1"} | "You" {"person": "2"};
NOUN -> "tickets";
VERB -> "have";
"""


def test_cfg():
    result = read_cfg(CFG_EXAMPLE)
    assert CFG([
        ("SENTENCE", Production([ProductionRef("PRONOUN"),
                                 ProductionRef("VERB"),
                                 ProductionRef("NOUN")])),
        ("PRONOUN", ProductionUnion([
            Terminal("I", features={"person": "1"}),
            Terminal("You", features={"person": "2"})
        ])),
        ("VERB", Terminal("have")),
        ("NOUN", Terminal("tickets"))
    ]) == result
