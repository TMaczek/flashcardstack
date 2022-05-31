from django.shortcuts import render, redirect
from django.contrib import messages
from main.forms import AddCardForm, AddLessonForm
from flashcardstack.models import FlashCard, Lesson


currentFlashcards = {}
# {'user' : [flashcard, flashcard, flashcard...], 'user2' : [f, f, f...]}

def clearCurrentFlashcards(request):
    print(currentFlashcards)
    currentFlashcards.pop(request.user, None)
    print(currentFlashcards)


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
            print("dziala")
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
            print("dziala")
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
    # current_user = request.user
    # data = FlashCard.objects.filter(lesson_id = lesson)
    # print(currentFlashcards)
    # current = None
    if currentFlashcards[request.user]:
        current = currentFlashcards[request.user][0]
        print(type(current))
        currentFlashcards[request.user].pop(0)
    else:
        return redirect('profile')
    return render(request, 'main/cards.html', {'data':current})
    

