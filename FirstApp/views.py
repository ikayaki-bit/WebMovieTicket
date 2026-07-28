import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # ← ここに AuthenticationForm を追加
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import User, Movie, Showtime, Seat, Booking

# --- 10作品のデータ（曜日指定: 月=0, 火=1, 水=2, 木=3, 金=4, 土=5, 日=6） ---
MOCK_MOVIES = [
    {"id": 1, "title": "Inception", "duration": 148, "hall": "hall 1", "weekdays": [0, 3]},
    {"id": 2, "title": "The Dark Knight", "duration": 152, "hall": "hall 1", "weekdays": [1, 4]},
    {"id": 3, "title": "Avengers", "duration": 143, "hall": "hall 1", "weekdays": [2, 5]},
    {"id": 4, "title": "Interstellar", "duration": 169, "hall": "hall 2", "weekdays": [0, 1]},
    {"id": 5, "title": "Toy Story", "duration": 102, "hall": "hall 2", "weekdays": [2, 3]},
    {"id": 6, "title": "Jurassic World", "duration": 124, "hall": "hall 2", "weekdays": [4, 5]},
    {"id": 7, "title": "It", "duration": 135, "hall": "hall 3", "weekdays": [0, 2]},
    {"id": 8, "title": "Night at the Museum", "duration": 108, "hall": "hall 3", "weekdays": [1, 3]},
    {"id": 9, "title": "Star Wars", "duration": 121, "hall": "hall 3", "weekdays": [4, 5]},
    {"id": 10, "title": "Minions", "duration": 90, "hall": "hall 1", "weekdays": [6]},
]

def get_14_days():
    """本日から14日間の日付リストを生成"""
    today = datetime.date.today()
    days = []
    weekdays_ja = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(14):
        d = today + datetime.timedelta(days=i)
        days.append({
            'date_str': d.strftime('%Y-%m-%d'),
            'display_str': f"{d.strftime('%m/%d')} ({weekdays_ja[d.weekday()]})",
            'weekday': d.weekday()
        })
    return days

def home(request):
    """初期表示はmovie_listと同じ処理に流す"""
    return movie_list(request)

def movie_list(request):
    """日付と映画の相互フィルタリングを行う"""
    selected_movie_id = request.GET.get('movie')
    selected_date_str = request.GET.get('date')

    all_dates = get_14_days()
    
    selected_movie = next((m for m in MOCK_MOVIES if str(m['id']) == selected_movie_id), None)
    selected_date_obj = next((d for d in all_dates if d['date_str'] == selected_date_str), None)

    available_movies = MOCK_MOVIES
    available_dates = all_dates

    if selected_date_obj and not selected_movie:
        available_movies = [m for m in MOCK_MOVIES if selected_date_obj['weekday'] in m['weekdays']]
    elif selected_movie and not selected_date_obj:
        available_dates = [d for d in all_dates if selected_movie['weekdays'].count(d['weekday']) > 0]
    elif selected_movie and selected_date_obj:
        available_movies = [m for m in MOCK_MOVIES if selected_date_obj['weekday'] in m['weekdays']]
        available_dates = [d for d in all_dates if selected_movie['weekdays'].count(d['weekday']) > 0]

    # 該当するShowtimeの取得
    target_showtime = None
    booked_seat_ids = []
    
    rows = ['A', 'B', 'C', 'D', 'E']
    cols = [1, 2, 3, 4, 5, 6, 7]

    if selected_movie and selected_date_str:
        target_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        
        movie_obj, _ = Movie.objects.get_or_create(
            id=selected_movie['id'],
            defaults={'title': selected_movie['title'], 'duration': selected_movie['duration']}
        )

        target_showtime, _ = Showtime.objects.get_or_create(
            movie=movie_obj,
            start_time__date=target_date,
            defaults={
                'start_time': datetime.datetime.combine(target_date, datetime.time(19, 0))
            }
        )

        if target_showtime:
            booked_seat_ids = list(Booking.objects.filter(showtime=target_showtime).values_list('seat_id', flat=True))

    # 各座席のID、番号、予約済みステータスをまとめたリストを作成
    seats_data = []
    has_available_seat = False

    for r in rows:
        for c in cols:
            seat_num = f"{r}{c}"
            seat_obj, _ = Seat.objects.get_or_create(seat_number=seat_num)
            is_booked = seat_obj.id in booked_seat_ids if target_showtime else False
            if not is_booked:
                has_available_seat = True
            seats_data.append({
                'id': seat_obj.id,
                'number': seat_num,
                'is_booked': is_booked
            })

    is_sold_out = target_showtime and not has_available_seat

    context = {
        'movies': available_movies,
        'available_dates': available_dates,
        'selected_movie': selected_movie,
        'selected_date': selected_date_str,
        'rows': rows, 
        'cols': cols, 
        'target_showtime': target_showtime,
        'booked_seat_ids': booked_seat_ids,
        'seats_data': seats_data,
        'is_sold_out': is_sold_out,
    }
    return render(request, 'FirstApp/home.html', context)

def seat_map(request):
    return render(request, 'FirstApp/seat_map_fragment.html')

def signup_view(request):
    """ユーザー登録"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'FirstApp/signup.html', {'form': form})

def login_view(request):
    """ログイン"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'FirstApp/login.html', {'form': form})

def logout_view(request):
    """ログアウト"""
    auth_logout(request)
    return redirect('home')

def create_booking(request):
    if request.method == 'POST':
        showtime_id = request.POST.get('showtime_id')
        seat_id = request.POST.get('seat_id')

        showtime = get_object_or_404(Showtime, id=showtime_id)
        seat = get_object_or_404(Seat, id=seat_id)

        # ログイン済み、未ログインに関わらず、FirstApp.models.User のインスタンスを取得・作成する
        if request.user.is_authenticated:
            user_name = request.user.username
        else:
            user_name = request.POST.get('user_name')
            if not user_name or not user_name.strip():
                return HttpResponse("<p style='color: red; font-weight: bold;'>エラー：名前を入力してください。</p>")
            user_name = user_name.strip()

        user, _ = User.objects.get_or_create(
            username=user_name, 
            defaults={'password': 'default_password'}
        )

        if Booking.objects.filter(showtime=showtime, seat=seat).exists():
            return HttpResponse("<p style='color: red; font-weight: bold;'>エラー：この座席はすでに予約されています。</p>")

        Booking.objects.create(
            showtime=showtime,
            seat=seat,
            user=user
        )

        return HttpResponse(f"""
        <div style="background-color: #d4edda; color: #155724; padding: 30px; border-radius: 8px; text-align: center;">
            <h2>Booking Confirmed.</h2>
            <p><strong>{user_name}</strong>, your booking for seat [ {seat.seat_number} ] has been confirmed.</p>
            <button onclick="location.reload()" style="margin-top: 15px; padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">Back to Home</button>
        </div>
        """)
    return HttpResponse(status=405)