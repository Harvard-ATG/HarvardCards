from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from harvardcards.apps.flash.models import Collection, Deck, Card, Field, Decks_Cards, Cards_Fields
from harvardcards.apps.flash.forms import FieldForm
from harvardcards.apps.flash import services, queries

def create(request):
    """Creates a card."""
    deck_id = queries.getCardDeckId(card_id)
    return redirect('deckIndex', deck_id)
    
def edit(request, card_id=None):
    """Edits a card."""
    deck_id = queries.getCardDeckId(card_id)
    return redirect('deckIndex', deck_id)

def delete(request, card_id=None):
    """Deletes a card."""
    deck_id = queries.getCardDeckId(card_id)
    services.delete_card(card_id)
    return redirect('deckIndex', deck_id)

