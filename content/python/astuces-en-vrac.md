Title: Astuces en vrac
Date: 2021-12-31 12:00
Modified: 2021-12-31 12:00
Category: Python
Tags: tips, tricks
Slug: astuces-en-vrac
Authors: Charles Monod-Broca


Python est sûrement le langage le plus élégant que je connaisse, et j'espère que cette page de trucs et astuces vous en convaincra également. Sans plus tarder, une liste non exhaustive, non ordonnée, de conseils pratiques pour gagner du temps de développement.

# Empaqueter et désempaqueter des listes

En python, vous pouvez empaqueter et désempaqueter des listes, avec l'opérateur `*`.
Il fonctionne de la même manière dans les deux sens. Exemple avec cette fonction:

## Empaqueter une liste d'arguments dans une liste: les bases

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

## Désempaqueter une liste en liste d'arguments: les bases

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

Ça fonctionne, bien sûr, mais ce n'est pas très pratique. Notamment si vous avez construit une liste vraiment longue, comme il peut arriver quand vous lisez les arguments depuis une chaîne de caractères dans un fichier.

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
Avec le désempaquetage des liste, et son opérateur `*`, vous pouvez faire l'inverse de ce qu'on a vu plus haut, à savoir décomposer une liste en arguments.

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

Et voilà, `line.split()` vous donne une liste, et vous la transformez en arguments positionnels avec le seul opérateur `*`. Je trouve ce gain en lisibilité et en temps de programmation plutôt important.

## Pour aller plus loin

### Désempaqueter dans un assignement

Il est aussi possible d'empaqueter et de désempaqueter des listes dans des expressions d'assignement.
Exemple, si vous avez un CSV avec cette structure:
`Nom, Prénoms..., Âge`

Notez les points de suspension après la colonne Prénoms. Dans votre CSV, il peut y avoir un ou plusieurs prénom par ligne, vous ne savez pas combien par avance. Or si vous voulez extraire du CSV une liste de personnes, sous la forme d'un dictionnaire; vous aimeriez avoir une liste pour le champ `Prénoms`, une chaîne de caractère pour le champ `Nom`, un entier pour le champ `Âge`... Bref plutôt compliqué. Mais en python, la solution est étonnamment simple. Voyez plutôt:

```python
with open("exemple.csv") as f:
    personnes = []
    for line in f:
        # *prenoms permet d'extraire sous forme de liste le 'reste' du désempaquetage
        nom, *prenoms, age = line.split(",")
        personne = {"Nom":nom, "Prénoms":prenoms, "Âge":age}
        personnes.append(personne)
```

Ici, on a désempaqueté le contenu de `line.split(",")` en le plaçant dans `nom`, `*prenom` et `age`.

Mais comme la taille du split peut être plus grande que trois, il faut collecter ce trop-plein sous peine d'une erreur. En effet, python ne peut pas deviner que seul le premier et le dernier champ (`nom` et `âge`) sont fixes, et que c'est `prenoms` qui varie. Grâce à l'opérateur `*`, vous dites au moment de désempaqueter la liste: "Prenez ce que vous voulez, je prendrai ce qui reste". Et comme la taille du reste est variable, python en fait une liste.

Notez qu'avec cette technique, vous ne pouvez avoir que trois parties: une ancre à gauche et/ou une ancre à droite, et une partie variable au milieu. Pour résumer:

=== "Ancres à droite"
        ```python
l = ["Boby","Jean-Eudes","Dupont",25,42]
#OK: trois ancres à droite: une seule façon de désempaqueter
*prenoms,nom,age,reponse = l
    ```
    ![Ancres à droite](https://imgur.com/2Mslfpq)

=== "Ancres à gauche et à droite"    
    ```
        #OK: une ancre à gauche, deux ancres à droite: une seule façon de désempaqueter, en mettant le reste dans noms
        prenom,*noms,age,reponse = l
    ```
    ![Ancres à gauche et à droite](https://imgur.com/wnpLEdC)

=== "Ancres à gauche"
    ```
        #OK: trois ancres à gauche: désempaqueter les trois premiers et laisser le reste comme une liste
        prenom1,prenom2,nom,*reponses = l
    ```
    ![Ancres à gauche](https://imgur.com/o4bFaU2)

=== "Erreur"
```python
    # Erreur: On demande de désempaqueter nom, et le reste de se partager entre gauche et droite. Mais comment ? Python ne peut pas deviner !
    *prenom,nom,*reponses = l
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

Utiliser `*args` et `**kwargs` dans vos fonctions les rendent beaucoup plus difficile à débugger. Utilisez les uniquement si vous savez ce que vous faites.
Un des gros inconvénients qui me vient en tête est l'absence d'erreur en cas de faute de frappe lorsque vous faites appel à un argument nommé qui n'est pas en paramètre d'une fonction. Exemple:

```python
def f(a,b,**kwargs):
    if "cassette" in kwargs:
        print("cassette aussi")

#J'ai mis trois s
f(5,6,casssette="k7")
```

Si vous exécutez ce code, il n'y aura aucune erreur. Mais vous vous attendiez à un comportement qui n'arrive pas, à savoir l'affichage de `cassette aussi`.

Le code est donc beaucoup moins facile à débugger puisque vous pensiez avoir fourni un argument, qu'il n'y a pas d'erreur, et que vous n'avez quand même pas le résultat attendu.

Dans l'autre sens, en revanche, je recommande chaudement l'utilisation du désempaquetage de dictionnaire. Avec un mini piège cependant...
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

# Formatter l'affichage d'un nombre entier avec les expressions régulières

Encore un cas pratique des expressions régulières !

Question: Comment formatter un nombre entier en insérant un espace tous les trois chiffres (mais de droite à gauche) ?

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

=== "Fonction"
    ```python
    import re

    def format_number(x):
        if not isinstance(x,int):
            return ""
        return re.sub(r"\d{3}",r"\g<0> ",str(x)[::-1])[::-1]
    ```

=== "Lambda"
    ```python
    import re

    formatter = lambda x:re.sub(r"\d{3}",r"\g<0> ",str(x)[::-1])[::-1]
    ```

