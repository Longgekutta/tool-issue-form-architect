default:
    @python main.py health

setup:
    @python main.py setup

test:
    @python main.py test

health:
    @python main.py health

clean:
    @python main.py clean

scaffold target="." owner="maintainer":
    @python main.py scaffold --target {{target}} --owner {{owner}}

lint target=".":
    @python main.py lint --target {{target}}
