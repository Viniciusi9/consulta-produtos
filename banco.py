"""Leitura e consulta dos produtos cadastrados."""

import csv
from pathlib import Path


ARQUIVO_PRODUTOS = Path(__file__).with_name("produtos.csv")


def carregar_produtos(caminho: Path = ARQUIVO_PRODUTOS) -> list[dict[str, str]]:
    """Lê o CSV e devolve os produtos como uma lista de dicionários."""
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo, delimiter=";"))


def buscar_produto(produtos: list[dict[str, str]], termo: str) -> dict[str, str] | None:
    """Encontra um produto por CPD exato ou por parte do nome."""
    termo = termo.strip().lower()

    if not termo:
        return None

    for produto in produtos:
        if termo.isdigit():
            if termo == produto["cpd"].strip().lower():
                return produto
        elif termo in produto["nome"].lower():
            return produto

    return None


def listar_sugestoes(
    produtos: list[dict[str, str]], termo: str, limite: int = 6
) -> list[dict[str, str]]:
    """Devolve até ``limite`` produtos cujo nome contém o texto informado."""
    termo = termo.strip().lower()

    if not termo or termo.isdigit():
        return []

    return [
        produto
        for produto in produtos
        if termo in produto["nome"].lower()
    ][:limite]
