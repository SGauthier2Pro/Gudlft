import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as clubs_file:
        list_of_clubs = json.load(clubs_file)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as competitions_file:
        list_of_competitions = json.load(competitions_file)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    try:
        club = [
            club
            for club in clubs
            if club['email'] == request.form['email']
        ][0]
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)
    except IndexError:
        flash("This email is not registered !")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [
        club_to_find
        for club_to_find in clubs
        if club_to_find['name'] == club
    ][0]
    found_competition = [
        competition_to_find
        for competition_to_find in competitions
        if competition_to_find['name'] == competition
    ][0]
    if found_club and found_competition:
        return render_template('booking.html',
                               club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    allready_booked_places = 0

    competition = [
        competition
        for competition in competitions
        if competition['name'] == request.form['competition']
    ][0]
    club = [
        club
        for club in clubs
        if club['name'] == request.form['club']
    ][0]

    if club['booked'] != {}:
        if competition['name'] in club['booked']:
            allready_booked_places = club['booked'][competition['name']]
        else:
            club['booked'][competition['name']] = allready_booked_places
    else:
        club['booked'][competition['name']] = allready_booked_places

    places_required = int(request.form['places'])

    if int(club['points']) >= places_required:
        if (allready_booked_places + places_required) <= 12:
            club['points'] = int(club['points']) - places_required
            competition['numberOfPlaces'] = \
                int(competition['numberOfPlaces']) - places_required
            club['booked'][competition['name']] = \
                places_required + allready_booked_places
            flash('Great-booking complete!')
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions)
        else:
            flash('You can not purchase more than 12 places per event!')
            return render_template('booking.html',
                                   club=club,
                                   competition=competition)
    else:
        flash('Not enough available points!')
        return render_template('booking.html',
                               club=club,
                               competition=competition)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
