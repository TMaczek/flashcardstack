from django.shortcuts import render, redirect
from django.contrib import messages
from main.forms import AddCardForm, AddLessonForm
from flashcardstack.models import FlashCard, Lesson
from datetime import date


currentFlashcards = {}
# {'user' : [flashcard, flashcard, flashcard...], 'user2' : [f, f, f...]}

def clearCurrentFlashcards(request):
    currentFlashcards.pop(request.user, None)


def reminder(request):
    lessons = Lesson.objects.filter(user = request.user)
    for lesson in lessons:
        cards = FlashCard.objects.filter(lesson = lesson.pk)
        for card in cards:
            if (date.today() - card.date_of_last_notice).days >= card.notice_lvl_in_days:
                messages.info(request, f'Lesson {lesson.title} needs repeating!')
                break

    
def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'main/home.html')


def addCard(request):
    if not request.user.is_authenticated:
        return redirect('main')

    if request.method == "POST":
        form = AddCardForm(request.POST)
        if form.is_valid():
            flashCard = FlashCard(
                lesson = Lesson.objects.get(pk = request.session["lesson_id"]),
                notice_lvl_in_days = 1,
                front_text = form.cleaned_data['front_text'],
                back_text = form.cleaned_data['back_text']
            )
            flashCard.save()
            messages.success(request, f'FlashCard: {flashCard} Created succesfuly')
            return redirect('addcard')

    else:
        form = AddCardForm()
    return render(request, 'main/addcard.html', {'form':form})

def addLesson(request):
    if not request.user.is_authenticated:
        return redirect('main')

    if request.method == "POST":
        form = AddLessonForm(request.POST)
        if form.is_valid():
            lesson = Lesson(user = request.user,
                                title = form.cleaned_data['title'],
                                description = form.cleaned_data['description']
                                )
            lesson.save()
            request.session["lesson_id"]=lesson.pk
            messages.success(request, f'Lesson: {lesson} Created succesfuly')
            return redirect('addcard')

    else:
        form = AddLessonForm()
    return render(request, 'main/addlesson.html', {'form':form})

def loadCards(request, lesson):
    currentFlashcards[request.user] = list(FlashCard.objects.filter(lesson_id = lesson))
    return redirect('showcards')


def showCards(request):
    if currentFlashcards[request.user]:
        current = currentFlashcards[request.user][0]
        request.session["card_id"] = current.id
        currentFlashcards[request.user].pop(0)
    else:
        return redirect('profile')
    return render(request, 'main/cards.html', {'data':current})

def correct(request):
    card = FlashCard.objects.get(id = request.session["card_id"])
    card.date_of_last_notice = date.today()
    card.notice_lvl_in_days = card.notice_lvl_in_days + 1
    card.save()
    return redirect('showcards')

def incorrect(request):
    card = FlashCard.objects.get(id = request.session["card_id"])
    card.date_of_last_notice = date.today()
    card.notice_lvl_in_days = 1
    card.save()
    return redirect('showcards')

def editLesson(request):
    clearCurrentFlashcards(request)
    request.session["lesson_id"]=None
    lessons = Lesson.objects.filter(user = request.user)
    return render(request, 'main/editlesson.html', {'lessons':lessons})

def editCards(request, lesson):
    flashCards = list(FlashCard.objects.filter(lesson_id = lesson))
    request.session["lesson_id"]=lesson
    return render(request, 'main/editcards.html', {'cards':flashCards})

def deleteLesson(request, lesson):
    lessonRecord = Lesson.objects.get(id = lesson)
    name = lessonRecord.title
    lessonRecord.delete()
    messages.success(request, f'Lesson: {name} Deleted succesfuly')
    return redirect('editlesson')

def deleteCard(request, card):
    FlashCard.objects.get(id = card).delete()
    messages.success(request, f'Card Deleted succesfuly')
    return redirect('/profile/editcards/' + str(request.session["lesson_id"]))