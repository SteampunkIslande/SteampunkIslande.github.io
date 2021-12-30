Title: Les expressions régulières (regex)
Category: Informatique
Tags: regular expressions, text analysis
Slug: les-expressions-regulieres
Authors: Charles Monod-Broca
Date:2021-12-30

Lorsque vous recherchez une expression dans un texte, il vous est sûrement déjà arrivé de réaliser que ce que vous voulez trouver correspond en réalité à un motif.

Par exemple, vous recherchez une adresse mail (inconnue) dans un document particulièrement long. Ou un numéro de téléphone. Ou tout autre texte dont vous ne connaissez pas à l'avance le contenu, mais seulement la forme, le motif. Pour une adresse mail par exemple, ce sera le nom de l'adresse, suivi d'un `@`, puis d'un nom de domaine (sous la forme `example.com`).

Bien sûr, cet exemple est très simplifié, [voici pour info](https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression) comment valider une adresse mail en se pliant aux standards en vigueur... Mais ce sera suffisant pour trouver n'importe quelle adresse mail plausible.

## Quelques exemples avec explications

Avant de commencer, petit point vocabulaire:

- Match: Lorsqu'on cherche un motif dans un texte, si le motif est présent, on se retrouve avec le match: c'est l'ensemble des caractères qui satisfont le critère de recherche. Ensuite, si on veut aller plus loin, on peut capturer des parties du motif, ce sont les groupes de capture (voir ci-dessous).

- Groupe de capture: Un des principaux avantages des expressions régulières est de pouvoir extraire du texte les caractères qui vous intéressent. C'est ce qu'on appelle la capture. Dans un programme utilisant une expression régulière (javascript, php, perl, python), on accède au contenu d'un groupe de capture grâce à son index. Exemple: `Tous les (chats|chiens) sont (gr[oi]s)` . Dans le groupe de capture 1, on trouve `chats` ou `chiens`. Dans le groupe de capture 2, on trouvera soit gros, soit gris. Et dans le groupe de capture 0, on trouvera tout le match. Notez que des groupes de capture peuvent être imbriqués, dans ce cas le numéro du premier groupe de capture sera celui dont la parenthèse ouvrante est le plus à gauche (c'est donc le groupe le plus à l'extérieur d'abord).

- Classe de caractère: Une description d'un ensemble de caractères possibles. Exemple: `[aeiouy]` pour matcher une voyelle, et `[^aeiouy]` pour matcher une consonne (*c.à.d.* pas une voyelle, le caractère `^` au début de la liste étant la négation). Il existe aussi des raccourcis, que je vous présente plus bas.

- Quantificateur: Une indication du nombre de répétition(s) du motif situé à gauche dudit quantificateur. Exemple: `[0-5]{6,10}` signifie "trouve un nombre entre 0 et 5, répété entre 6 et 10 fois".

### Numéro de téléphone français

La première chose qui effraie la plupart des débutants, c'est la taille de certaines expressions régulières. Des dizaines de caractères à la suite, sans saut de ligne, qui, sans documentation, sont tout sauf explicites. Et au fond, même avec un bon entraînement, lire et comprendre une expression régulière que l'on n'a pas soi-même écrite peut être difficile.

Mais commençons ! Voici par exemple une expression régulière pour trouver un numéro de téléphone en France:

```regex
(0[1-79]).?(\d{2}).?(\d{2}).?(\d{2}).?(\d{2})
```

Décomposons cette regex. Entre parenthèses, on indique que l'on veut "capturer" le contenu du motif trouvé à l'intérieur. Ici, c'est `0[1-79]`.
Et pour expliquer ce motif, on a seulement besoin de comprendre les classes de caractères. Ici, `0[1-79]` recherche littéralement un 0, suivi d'un nombre soit entre 1 et 7 (signifié par le tiret `-`) ou encore un `9`. Donc les crochets `[]` permettent de trouver un caractère parmi ceux indiqués, avec la possibilité de donner des intervalles.

Exemple:

```regex
[a-zAZ]
```

Va matcher n'importe quelle lettre, minuscule ou majuscule, mais sans accent. Pour ajouter quelques accents:

```regex
[a-zAZéèêàù]
```

Maintenant que vous avez compris que `(0[1-79])` capturait les deux premier chiffres d'un numéro de téléphone français, passons à la suite de l'expression.

Nous avons, après ce premier groupe de capture, `.?`. Le point est un caractère spécial qui matche n'importe quel caractère (sauf les retours à la ligne).
Ensuite, nous avons un quantificateur. Celui-ci est le point d'interrogation. Il signifie zéro ou un. Il s'écrit aussi `{0,1}`, qui est la syntaxe complète des quantificateurs. Alors pourquoi chercher un caractère optionnel juste après les premiers chiffres ? Simplement parce que certaines personnes ajoutent un caractère tous les deux chiffres quand ils donnent leur numéro de téléphone. Certains ne séparent pas, d'autres mettent un point, d'autres encore un slash... Bref on pourrait aussi écrire `[/.]?`, mais ici on veut prévoir tous les cas de figure. Notez ici qu'entre les crochets, pas besoin d'échapper le point. En effet, dans une classe de caractère, ajouter une telle "carte blanche" n'aurait aucun sens.

Viennent ensuite quatre répétitions de `.?(\d{2})`. D'abord, le caractère de séparation optionnel (`.?`). Celui-ci n'est pas intéressant, on ne le capture pas.

En revanche, ce qui suit nous intéresse: on veut trouver deux chiffres. Pour cela, on utilise une classe de caractères un peu spéciale, appelée méta séquence. C'est juste un antislash pour échapper le d qui suit. "d" pour "digit", soit chiffre en anglais. Entre crochet, le quantificateur. Si on met un seul chiffre, cela signifie "exactement n fois". Si on veut entre 0 et 5 fois la classe qui précède, on va séparer par une virgule, soit `{0,5}`. Et si on veut entre 1 et une infinité, c'est soit `{1,}`, soit son équivalent raccourci `+`.

Et voilà comment interpréter une expression régulière !

### Adresse mail

Autre exemple, pour une adresse électronique:

```regex
(\S+)@(\S+)\.(\S+)
```

Cette regex fait apparaître une méta séquence que je ne vous ai pas présenté plus haut, les espaces. Notez que `\s` matche n'importe quel caractère d'espace (tabulation, espace, retour à la ligne, et autres caractères ésotériques qui peuvent vous donner des bugs invisibles ^^).

À l'inverse, `\S` matche tout caractère qui n'est pas un espace. Donc cette regex n'exclut pas beaucoup d'adresses mail invalides, mais trouvera la plupart des adresses mail plausibles.

Ci-dessous un tableau qui présente les méta séquences que j'utilise le plus (personnellement). Ce n'est pas du tout une liste exhaustive.

{! content/informatique/regex_metasequences_table.html !}

Ces méta séquences s'utilisent exactement comme n'importe quelle classe de caractère (`[a-zA-Zéèàç]`), vous pouvez les utiliser avec des quantificateurs (`{0,+}` ou `*`).

Celle-ci est sans doute beaucoup trop permissive (elle ne permet que de s'assurer qu'il n'y a pas d'espace, qu'il y a bien un `@` et un nom de domaine).
Toutes les adresses mail valides seront détectées par ce motif, mais tous les textes détectés par ce motif ne seront pas des adresses mail valides.

N'utilisez donc pas cette expression régulière pour être certain qu'une adresse mail est valide ! S'il y a détection par ce motif, au mieux l'adresse est plausible.

## Comment construire une expression régulière

Maintenant que vous avez compris comment fonctionnent des expression régulières existantes, voyons comment les créer. Nous allons voir le cas simple, linéaire, avec des matchs qui ne se chevauchent pas.

Construire soi-même une expression régulière n'est pas si complexe que ça en a l'air, en tout cas comparé au résultat vous risquez de vous étonner vous-même !

Pour commencer, vous pouvez "ancrer" votre expression régulière dans le texte à rechercher. 

Pour cela, vous avez deux opérateurs: `^` et `$`.

Pour trouver un morceau de texte qui commence par votre motif:

```regex
^Les chiens sont (.+)
```

Pour trouver le motif ci-dessus, toutes les lignes commençant par `Les chiens sont ` vont être trouvées. Puis ce qui suit sera capturé dans le groupe 1, le motif étant la carte blanche, répétée autant de fois que possible.

De même, vous pouvez chercher un motif qui termine une ligne, dans ce cas:

```regex
(.+) intelligents\.$
```

Dans cette situtation, toutes les lignes finissant par ` inteeligents.` seront trouvées, et ce qui précède sera capturé dans le groupe 1.

Pour finir, construire une expression régulière, c'est juste définir l'aspect d'un motif en utilisant les trois éléments vus plus haut: capturer ce qui vous intéresse, définir les valeurs possibles avec des classes de caractères, et quantifier ces dernières.

Exemple pour trouver dans un fichier de configuration, toutes les variables contenant `site`:
`(.*site.*)=(.+)`

## Quelques conseils en vrac

Lorsque vous utilisez une expression régulière, adaptez le degré de complexité à l'objectif que vous voulez atteindre. Comme dit plus haut, demandez-vous si vous préférez prendre le risque de trouver des faux positifs ou plutôt des faux négatifs. Si par exemple vous utilisez une expression régulière pour chercher une adresse mail dans un gros fichier texte, capturer des adresses mails non valides n'aura pas trop de conséquences, vous pourrez toujours les valider avec des outils tiers (ou une expression régulière plus restricive pour affiner la recherche). En revanche, si c'est pour vérifier qu'un utilisateur a bien rentré une adresse mail, vous ne pouvez pas vous permettre d'attraper des faux positifs (*i.e.* accepter une adresse mail invalide).

Personne n'aime créer ou maintenir des expressions régulières... Heureusement, il existe [un site Internet très pratique](https://regex101.com/) (que j'ai d'ailleurs utilisé pour écrire cet article) qui permet de:

- Tester vos expressions régulières
- Générer des morceaux de code (utilisant votre regex) dans plusieurs langages de programmation
- Expliquer la regex que vous êtes en train de tester
- Et plus encore...

Vous avez même un pense-bête avec tous les opérateurs supportés dans le moteur d'expressions régulières que vous avez choisi.

