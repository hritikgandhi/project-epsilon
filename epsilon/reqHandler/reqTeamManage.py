from epsilonModules.ModTeam import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user


def act_on_employee(mysql: MySQL):
    """
    Handler for delete/promot an employee in team.
    :param mysql: mysql db.
    :return redirect to display_team
    """
    if request.method == 'POST':
        # id2 is either tid or rid
        op, uid, tid, rid = request.form['submit'].split(".")
        if op == 'r':
            remove_from_team(mysql, tid, uid, rid)
        elif op == 'p':
            promote_admin(mysql, tid, uid, rid)
    return redirect(url_for('displayteam', tid=tid))


def render_display_team(mysql: MySQL):
    """
    Handler for displaying team members in a team.
    :param mysql: mysql db.
    :param tid: tid of team.
    :return template for display team.
    """
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        user_details = get_members(mysql, tid)
        return render_template('display_team.html', userDetails=user_details)
    except Exception as e:
        return render_template('display_team.html', message=e)


def render_join_team_request(mysql: MySQL):
    """
    Handler for join team request.
    :param mysql: mysql db.
    :param tid: tid of team.
    :return template for join team request.
    """
    message = ""
    if request.method == 'POST':
        action = request.form["action"].split("_")
        if action[0] == "A":
            message = team_request_accept(mysql, action[1])
        elif action[0] == "D":
            message = team_request_decline(mysql, action[1])
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        data, company_name = get_join_requests(mysql, tid)
        if len(data) == 0:
            return render_template("join_team_request.html",
                                   message="No pending requests!", tid=tid,
                                   company_name=company_name)
        return render_template("join_team_request.html", data=data, tid=tid,
                               message=message, company_name=company_name)
    except Exception as e:
        return render_template("join_team_request.html",
                               message=e)

def render_team_mgmt_combined(mysql: MySQL):
    """
    Handler for page containing both join 
    team request and team management
    :param: mysql: mysql db
    :return: template for combined page
    """
    message = ""
    if request.method == 'POST':
        action = request.form["action"].split("_")
        # action -> (request wanted, req id, tid)
        if action[0] == 'A':
            message = team_request_accept(mysql, action[1])
        elif action[0] == 'D':
            message = team_request_decline(mysql, action[1])
        # action -> (request wanted, uid, tid, rid)
        elif action[0] == 'P':
            message = promote_admin(mysql, action[2], action[1], action[3])
        elif action[0] == 'R':
            message = remove_from_team(mysql, action[2], action[1], action[3])
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        rid = teams[0].rid
        print(rid)
        data, company_name = get_join_requests(mysql, tid)
        user_details = get_members(mysql, tid)
        if len(data) == 0:
            return render_template("team_management_combined.html",
                                   message="No pending requests!", tid=tid,
                                   company_name=company_name, userDetails=
                                   user_details, role=rid)
        return render_template("team_management_combined.html", data=data, tid=tid,
                               message=message, company_name=company_name, 
                               userDetails=user_details, role=rid)
    except Exception as e:
        return render_template("team_management_combined.html",
                               message=e)
