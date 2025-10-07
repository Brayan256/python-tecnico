import csv
import json
import smtplib
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from typing import List, Dict, Optional

TEAM = [
    "Agustín Alcántara",
    "Jorge Medrano",
    "Luis de la Rosa",
    "Norberto Diaz",
    "Juan Carlos Soriano",
    "Juan Chagoya",
    "Cristóbal Andrade",
    "Eugenio Ramírez",
    "Isaac Viveros",
    "Juan Jesús Trujano",
]

SMTP_HOST = "smtp.test.com"
SMTP_PORT = 465
SMTP_USER = "#####"
SMTP_PASS = "########"
MAIL_FROM = "Test"
MAIL_TO = ["email.com"]

@dataclass
class WeekRole:
    week_no: int
    start: date
    end: date
    headline: str
    nex: str
    standby: List[str]

def first_monday(year: int) -> date:
    d = date(year, 1, 1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return d

def mondays_of_year(year: int) -> List[date]:
    mons = []
    d = first_monday(year)
    while d.year == year:
     mons.append(d)
     d += timedelta(weeks=1)
    return mons

def generate_schedule(year: int, team: List[str] = TEAM) -> List[WeekRole]:
    mons = mondays_of_year(year)
    schedule: List[WeekRole] = []
    n = len(team)
    for i, monday in enumerate(mons, start=1):
        start = monday
        end = start + timedelta(days=6)
        headline = team[(i - 1) % n]
        nex = team[i % n]
        standby = [p for p in team if p != headline]
        schedule.append(WeekRole(i, start, end, headline, nex, standby))
    return schedule

def export_csv(schedule: List[WeekRole], path: str) -> None:
   with open(path, "w", newline="", encoding="utf-8") as f:
      w = csv.writer(f)
      w.writerow(["Semana", "Inicio (Lun)", "Fin (Dom)", "Headline", "Next", "StandBy"])
      for row in schedule:
         w.writerow([
            row.week_no,
            row.start.isoformat(),
            row.end.isoformat(),
            row.headline,
            row.nex,
            "; ".join(row.standby),
         ])

def build_email_body(role: WeekRole) -> str:
    def fmt(d: date) -> str:
        meses = ["enero","febrero","marzo","abril","mayo","junio",
                 "julio","agosto","septiembre","octubre","noviembre","diciembre"]
        return f"{d.day:02d} de {meses[d.month-1]} de {d.year}"

    inicio = role.start
    fin = role.end
    lines = []
    lines.append(f"Semana {role.week_no} — Guardia de {fmt(inicio)} a {fmt(fin)}")
    lines.append("")
    lines.append(f"Titular: {role.headline}")
    lines.append(f"Siguiente guardia: {role.nex}")
    lines.append("")
    lines.append("En espera:")
    for p in role.standby:
        lines.append(f"  - {p}")
    lines.append("")
    lines.append("Nota: La guardia cubre de lunes 00:00 a domingo 23:59.")
    return "\n".join(lines)


def send_email(subject: str, body: str,
               to_addrs: List[str] = MAIL_TO,
               from_addr: str = MAIL_FROM) -> None:
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as s:
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(SMTP_USER, to_addrs, msg.as_string())

@dataclass
class Absence:
    person: str
    start: date
    end: date


def apply_absences(schedule: List[WeekRole],
                   absences: List[Absence],
                   team: List[str] = TEAM) -> None:

    by_person: Dict[str, List[Absence]] = {}
    for a in absences:
        by_person.setdefault(a.person, []).append(a)

    def is_absent(person: str, start: date, end: date) -> bool:
        arr = by_person.get(person, [])
        for a in arr:
            if not (end < a.start or start > a.end):
                return True
        return False

    for wk in schedule:
        if is_absent(wk.headline, wk.start, wk.end):
            replacement: Optional[str] = None
            for cand in wk.standby:
                if not is_absent(cand, wk.start, wk.end):
                    replacement = cand
                    break
            if replacement:
                wk.headline = replacement
                wk.nex = next_person_after(schedule, wk.week_no, team, wk.headline)
                wk.standby = [p for p in team if p != wk.headline]

def next_person_after(schedule: List[WeekRole], week_no: int,
                      team: List[str], headline: str) -> str:
    idx = team.index(headline)
    return team[(idx + 1) % len(team)]


def apply_swaps(schedule: List[WeekRole],
                swaps: List[Dict[str, int]]) -> None:

    by_week = {wk.week_no: wk for wk in schedule}
    for s in swaps:
        a = by_week.get(s["week"])
        b = by_week.get(s["with_week"])
        if a and b:
            a.headline, b.headline = b.headline, a.headline
            tmp = a.nex
            a.nex = b.nex
            b.nex = tmp
            a.standby = [p for p in TEAM if p != a.headline]
            b.standby = [p for p in TEAM if p != b.headline]