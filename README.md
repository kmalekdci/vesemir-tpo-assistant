# Vesemir, asystent TPO

TPO chce mieć do dyspozycji czat, który pozwoli mu zadawać pytania dotyczące różnych kwestii związanych z zarządzaniem produktem, zespołem i procesami.

## Etapy

Podejście „progressive enhancement” dla AI. Najpierw wartość → potem kontekst → potem automatyzacja.

### Chat ekspercki (LLM + prompt engineering, bez danych firmowych)

#### Idea

Budujesz czat jako eksperta TPO, który:

- zna dobre praktyki
- pomaga podejmować decyzje
- wspiera w analizie

Nie ma dostępu do danych firmy — działa jak „coach + konsultant”.

#### Jak działa

- System prompt zawiera:
    - kontekst platformy (np. CMS dla newsów)
    - rolę TPO
    - standardy pracy (Scrum, Kanban, DevOps)
- opcjonalnie:
    - pamięć sesji (rozmowy)
    - proste struktury (np. cele, backlog wpisywany ręcznie)

#### Zalety

- Bardzo proste wdrożenie
- Zero ryzyka wycieku danych
- Szybkie działanie
- Dobre wsparcie „myślowe”

#### Wady

- Brak wiedzy o realnych projektach
- Odpowiedzi mogą być zbyt ogólne
- TPO musi sam dostarczać kontekst

#### Kiedy ma sens

- Na start
- Jako „drugi mózg” do decyzji
- Do pracy strategicznej

### Manual Context Injection (półautomatyczny RAG)

#### Idea

Zamiast automatycznego eksportu:
👉 TPO sam wkleja dane do czatu (lub wrzuca pliki)

System:
- analizuje dostarczony kontekst
- odpowiada na jego podstawie

#### Jak działa

- użytkownik:
    - wkleja ticket / roadmapę / opis problemu
- system:
    - robi parsing
    - opcjonalnie zapisuje do tymczasowej pamięci
    - odpowiada

Można dodać:
- lokalną „pamięć sesji”
- tagowanie informacji

#### Zalety

- 100% zgodne z polityką (user decyduje co trafia do AI)
- zawsze aktualne dane
- brak potrzeby integracji
- dużo prostsze niż pełny RAG

#### Wady

- manualna praca użytkownika
- brak historii (jeśli nie zapisujesz)
- mniej wygodne przy dużej skali

#### Kiedy ma sens

- gdy dane są wrażliwe
- gdy eksport jest zabroniony
- gdy TPO pracuje na konkretnych case’ach
