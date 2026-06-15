from dataclasses import dataclass
import json


@dataclass
class ScoreEntry:
    name: str
    score: int


MAX_SCORES: int = 10


def add_highscore(scores: list[ScoreEntry],
                  new_name: str,
                  new_score: int) -> None:
    """
    Ajoute le nouveau score avec le nom du joueur a la liste des highscores.

    Args:
        scores: la liste contenant les highscores
        new_name: le nom du nouveau joueur
        new_score: le score du nouveau joueur
    Returns:
        None.
    """
    current_score: ScoreEntry = ScoreEntry(new_name, new_score)
    # On verifie la liste de score ne contient pas
    # plus de 10(MAX_SCORES) occurences
    if len(scores) < MAX_SCORES:
        scores.append(current_score)
    else:
        # On verifie que le nouveau score est superieur
        # au dernier score de la liste.
        if current_score.score > scores[-1].score:
            # On ajoute le nouveau score a la liste.
            scores.append(current_score)
    scores.sort(key=lambda s: s.score, reverse=True)
    # On verifie si la nouvelle liste contient
    # plus de 10(MAX_SCORES) occurences.
    if len(scores) > MAX_SCORES:
        # Si c'est le cas, on supprime la derniere occurence
        # (score le plus faible) de la liste.
        scores.pop()


def sanitize_name(name: str) -> str:
    """
    Verifie et corrige le nom du joueur.

    Args:
        name: le nom du joueur
    Returns:
        un str correspondant au nom du joueur valide.
    """
    new_name: str = ""
    for char in name:
        if char.isalnum() or char == " ":
            new_name = new_name + char
    # On supprime les espaces en debut et fin de chaine de caracteres.
    correct_name: str = new_name.strip()
    # Si le nom est vide, on retourne UNKNOWN en tant que nouveau nom.
    if not correct_name:
        return "UNKNOWN"
    # On check si le nom depasse la limite de 10 caracteres.
    if len(correct_name) > 10:
        # Si c'est le cas, on garde les 9 premiers caracteres
        # et on ajoute ~ pour le 10eme.
        final_name: str = correct_name[0:9] + "~"
    else:
        # Sinon, on renvoie le nom tel quel.
        return correct_name
    return final_name


def load_highscores() -> list[ScoreEntry]:
    """
    Charge les highscores a partir d'un fichier JSON.

    Args:
        None
    Returns:
        une liste contenant les scores au format ScoreEntry
    """
    score_table: list[ScoreEntry] = []
    # On essaye d'ouvrir le fichier JSON contenant les scores.
    try:
        with open("highscores.json", "r") as file:
            raw_data: list[dict[str, str | int]] = json.load(file)
            # On verifie que les donnees sont ok.
            for entry in raw_data:
                # On corrige le nom si besoin avec sanitize_data
                # et on le recupere.
                c_name: str = sanitize_name(str(entry["name"]))
                # On recupere le score en forcant le format en int
                # pour satisfaire mypy.
                c_score: int = int(entry["score"])
                # On verifie si le score est bien un entier positif.
                if c_score < 0:
                    # Si ce n'est pas le cas, on le remplace par 0.
                    c_score = 0
                current_sc: ScoreEntry = ScoreEntry(c_name, c_score)
                # On ajoute le nom/score a la liste.
                score_table.append(current_sc)
        return score_table
    # Si la table de score est corrompue ou n'a pas ete trouvee,
    # on renvoie une liste vide.
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_highscores(scores: list[ScoreEntry]) -> None:
    """
    Remplace l'ancienne liste des highscores par la nouvelle
    dans le fichier JSON contenant la liste des highscores.

    Args:
        scores: la liste contenant le nom du joueur et son score
    Returns:
        None.
    """
    data_to_save: list[dict[str, str | int]] = []
    # On extrait le nom du joueur et son score de la liste.
    for entry in scores:
        new_dict: dict[str, str | int] = {"name": entry.name,
                                          "score": entry.score}
        data_to_save.append(new_dict)
    # On essaye d'ouvrir le fichier JSON contenant
    # les highscores en mode ecriture.
    try:
        with open("highscores.json", "w") as file:
            # Si ok, on remplace le contenu du fichier JSON
            # par le nouveau tableau.
            json.dump(data_to_save, file, indent=4)
    except (OSError, PermissionError) as e:
        print(f"Error when trying to save high score: {e}")
