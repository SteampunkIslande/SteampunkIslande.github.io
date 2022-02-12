Title: Astuces en vrac
Date: 2021-12-31 12:00
Modified: 2022-02-12 23:55
Category: Python
Tags: tips, tricks
Slug: astuces-en-vrac
Authors: Charles Monod-Broca

Python est sûrement le langage le plus élégant que je connaisse, et j'espère que cette page de trucs et astuces vous en convaincra également. Sans plus tarder, une liste non exhaustive, non ordonnée, de conseils pratiques pour gagner du temps de développement.

# Empaqueter et désempaqueter des listes

En python, vous pouvez empaqueter et désempaqueter des listes, avec l'opérateur `*`.
Il fonctionne de la même manière dans les deux sens. Exemple avec cette fonction:

## Empaqueter une liste d'arguments dans une liste

```python
def f(*args):
    print(args)
```

Pour appeler cette fonction, vous pouvez passez autant d'arguments que vous voulez. À l'exécution:
```python
>>> f(1,2,3)
[1, 2, 3]
```

Ainsi, avec cette étoile, vous avez empaqueté la liste des arguments dans une liste appelée args. Ce qui vous permet de passer autant d'arguments positionnels que vous voulez, et pour y accéder vous pouvez considérer `args` comme n'importe quelle liste. Et vous n'êtes pas obligé de l'appeler `args`, c'est juste une convention.

## Désempaqueter une liste en liste d'arguments

À l'inverse, vous pouvez désempaqueter une liste. Prenons cette nouvelle fonction, qui prend trois arguments en paramère:

```python
def f(a,b,c):
    print(a,b,c)
l = [1, 2, 3]
```

Dans ce cas, on doit passer plusieurs arguments à f. L'approche naïve serait:

```python
f(l[0],l[1],l[2])
```

Ça fonctionne, bien sûr, mais ce n'est pas très pratique. Notamment si vous avez construit une liste vraiment longue, accéder aux éléments un par un peut être fastidieux et source d'erreurs.

Exemple:
```python

def ma_fonction(first, second, third='default_value'):
    # Peu importe ce que fait la fonction elle prend trois arguments
    ...

with open("example") as f:
    for line in f:
        # Chaque ligne contient bien les arguments que je veux, séparés par des virgules
        mes_arguments = line.split(",")
        ma_fonction(mes_arguments[0],mes_arguments[1],mes_arguments[2])

```

Beaucoup trop long... Imaginez si `ma_fonction` prenait plus d'arguments... Vous allez en taper du code !
Avec le désempaquetage des listes, et son opérateur `*`, vous pouvez faire l'inverse de ce qu'on a vu plus haut, à savoir décomposer une liste en arguments.

Ce qui donne:

```python
def ma_fonction(first, second, third='default_value'):
    # Peu importe ce que fait la fonction elle prend trois arguments
    ...

with open("example") as f:
    for line in f:
        # Chaque ligne contient bien les arguments que je veux, séparés par des virgules
        ma_fonction(*line.split(","))
```

Et voilà, `line.split()` vous donne une liste, et vous la transformez en arguments positionnels avec le seul opérateur `*`. Plus lisible et bien plus efficace.

## Pour aller plus loin

### Désempaqueter dans un assignement

Il est aussi possible d'empaqueter et de désempaqueter des listes dans des expressions d'assignement.

Typiquement, si vous avez un CSV avec un nombre de colonnes variable. Exemple:

```
Prénom, Âge, Professions
Boby, 24, Bioinformaticien
Alexandre, 27, Acteur, Réalisateur, Scénariste, Photographe, Musicien
Roland, 23, Community Manager, Chômeur
```

Notez qu'une même personne peut avoir un nombre variable de professions. Or si vous voulez extraire du CSV une liste de personnes et que vous voulez pour chaque personne son nom, son âge et ses professions, comment allez-vous vous y prendre ?

Une solution possible est décrite ci-dessous:

```python
personnes = []
with open("exemple.csv") as f:
    header = next(f)
    for line in f:
        # *prenoms permet d'extraire sous forme de liste le 'reste' du désempaquetage
        prenom, age, *professions = line.split(",")
        personne = {"Prénom":prenom, "Âge":age, "Profession(s)":professions}
        personnes.append(personne)
```

Notez que dans cette approche, la magie opère de manière très discrète: juste `*professions` qui permet de récupérer tout ce qui n'a pas pu être désempaqueté.
Vous pouvez tester ce petit script en reprenant le CSV proposé plus haut, et en affichant la variable `personnes`.

Remarque:

Il est possible de placer cette wildcard où vous voulez dans l'assignement, mais une seule fois maximum !
Exemple:
```python
prenom, nom, *notes, age = line.split(",")
*prenoms, nom, age = line.split(",")
```

### Passer un dictionnaire en arguments nommés

Dernier cas de figure, vous avez un dictionnaire dont les clés correspondent parfaitement aux noms des arguments de votre fonction.

Exemple:
```python
d = {"a":5,"b":3}
def f(a,b):
    print(a+b)
```

Pour passer votre dictionnaire en argument de f, vous pouvez le désempaqueter avec un opérateur similaire à celui pour désempaqueter une liste. Comme ceci:

```python
d = {"a":5,"b":3}
def f(a,b):
    print(a+b)

f(**d)
```

L'opérateur `**` permet de transformer un dictionnaire en arguments nommés.

### Accepter n'importe quel argument nommé dans une fonction

Dans une fonction, pour accepter n'importe quel argument nommé:

```python
def f(**kwargs):
    if "a" in kwargs:
        print("named argument a was passed to f :",kwargs["a"])
    if "b" in kwargs:
        print("named argument b was passed to f :",kwargs["b"])

f(a=2,b=3)

```

Notez que la syntaxe est très proche de celle utilisée pour les arguments positionnels. On peut même les mélanger:

```python
def f(*args,**kwargs):
    print(f"Args. positionnels:\n{args}\nArgs. nommés:\n{kwargs}")

f(1,2,3,x=3,y=4,z=5)

# Résultat:
Args. positionnels:
(1, 2, 3)
Args. nommés:
{'x': 3, 'y': 4, 'z': 5}
```

### Quelques pièges à éviter

Utiliser `*args` et `**kwargs` dans vos fonctions les rendent beaucoup plus difficile à débugger. Utilisez-les uniquement si vous savez ce que vous faites.
Un des gros inconvénients qui me vient en premier est l'absence d'erreur en cas de faute de frappe lorsque vous faites appel à un argument nommé qui n'est pas en paramètre d'une fonction. Exemple:

```python
def f(a,b,**kwargs):
    if "color" in kwargs:
        print("color set")

#J'ai mal orthographié color
f(5,6,colour="red")
```

Si vous exécutez ce code, il n'y aura aucune erreur, bien que vous vous attendiez à voir affiché `color set`.

Le code est donc beaucoup moins facile à débugger puisque vous pensiez avoir fourni un argument, qu'il n'y a pas d'erreur, et que vous n'avez quand même pas le résultat attendu.

Dans l'autre sens, en revanche, je recommande fortement l'utilisation du désempaquetage de dictionnaire. Avec un mini piège cependant...
Pour une fonction documentée:

```python
def f(a,b,c):
    ...

d={"a":1,"b":3,"c":5}
# Tout marche...
f(**d)

#... 'a' étant le premier argument, mais aussi présent dans d
#... quelle valeur doit-il prendre ?
f(6,**d)

```

Ce que me dit IPython:
<pre><font color="#CC0000">TypeError</font>: f() got multiple values for argument &apos;a&apos;</pre>

Ce qui est normal, vous avez passé une valeur à `a` comme argument positionnel, puis le reste a été passé en arguments nommés. Comme `a` est aussi défini dans `d`, python ne sait pas quelle valeur choisir et vous renvoie une erreur.

# Formater l'affichage d'un nombre entier avec les expressions régulières

Encore un cas pratique des expressions régulières !

Question: Comment formater un nombre entier en insérant un espace tous les trois chiffres (mais de droite à gauche) ?

Réponse: Avec une expression régulière et la fonction `sub`.

Première étape: comprendre la fonction `re.sub`. En python:
```python
>>>import re
>>>re.sub(r"\d{3}",r"\g<0> ",str(1789))
178 9
```

L'expression régulière ci-dessus recherche des groupes de trois lettres. Il n'y a pas de groupe de capture, mais dans la chaîne de remplacement, on demande le groupe 0 suivi d'un espace. Rappelez-vous, si une expression régulière matche, le groupe de capture 0 représente le match complet. Dans notre exemple, il y a quatre chiffres. Donc il y a un seul match de trois lettres, situé au début. Ça, on ne peut rien y faire, c'est le fonctionnement normal des expressions régulières.

Mais on peut ruser. Par exemple, en inversant la chaîne que l'on veut matcher. En python, inverser un itérable est beaucoup trop facile:

```python
>>>"1789"[::-1]
"9871"
```

Et maintenant ?
```python
>>>import re
>>>re.sub(r"\d{3}",r"\g<0> ",str(1789)[::-1])
987 1
```

On a bien séparé les centaines, les dizaines et les unités des milliers. Mais à l'envers. Donc on a juste à retourner la chaîne obtenue:
```python
>>>import re
>>>re.sub(r"\d{3}",r"\g<0> ",str(1789)[::-1])[::-1]
1 789
```

Et voilà! En prime, deux appelables issus de cette astuce (vous choisissez, fonction ou fonction anonyme):

```python fct_label="Fonction"
import re

def format_number(x):
    if not isinstance(x,int):
        return ""
    return re.sub(r"\d{3}",r"\g<0> ",str(x)[::-1])[::-1]
```

```python fct_label="Lambda"
import re

formatter = lambda x:re.sub(r"\d{3}",r"\g<0> ",str(x)[::-1])[::-1]
```
