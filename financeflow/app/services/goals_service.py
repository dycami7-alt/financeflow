from typing import List, Optional
from app.database import get_connection
from app.models.goals import Goal, GoalCreate, GoalUpdate


def create_goal(user_id: int, goal_data: GoalCreate) -> Goal:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO goals (user_id, title, target_amount, deadline, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, goal_data.title, goal_data.target_amount, goal_data.deadline, goal_data.status)
    )

    goal_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return Goal(
        id=goal_id,
        user_id=user_id,
        title=goal_data.title,
        target_amount=goal_data.target_amount,
        current_amount=0.0,
        deadline=goal_data.deadline,
        status=goal_data.status
    )


def get_goals_by_user(user_id: int) -> List[Goal]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM goals WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )

    rows = cursor.fetchall()
    connection.close()

    return [Goal(**dict(row)) for row in rows]


def get_goal_by_id(goal_id: int, user_id: int) -> Optional[Goal]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM goals WHERE id = ? AND user_id = ?",
        (goal_id, user_id)
    )

    row = cursor.fetchone()
    connection.close()

    if row:
        return Goal(**dict(row))
    return None


def update_goal(goal_id: int, user_id: int, goal_data: GoalUpdate) -> Optional[Goal]:
    connection = get_connection()
    cursor = connection.cursor()

    # Build update query dynamically
    update_fields = []
    values = []

    if goal_data.title is not None:
        update_fields.append("title = ?")
        values.append(goal_data.title)

    if goal_data.target_amount is not None:
        update_fields.append("target_amount = ?")
        values.append(goal_data.target_amount)

    if goal_data.current_amount is not None:
        update_fields.append("current_amount = ?")
        values.append(goal_data.current_amount)

    if goal_data.deadline is not None:
        update_fields.append("deadline = ?")
        values.append(goal_data.deadline)

    if goal_data.status is not None:
        update_fields.append("status = ?")
        values.append(goal_data.status)

    if not update_fields:
        return get_goal_by_id(goal_id, user_id)

    query = f"UPDATE goals SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
    values.extend([goal_id, user_id])

    cursor.execute(query, values)
    connection.commit()
    connection.close()

    return get_goal_by_id(goal_id, user_id)


def delete_goal(goal_id: int, user_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM goals WHERE id = ? AND user_id = ?",
        (goal_id, user_id)
    )

    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()

    return deleted


def complete_goal(goal_id: int, user_id: int) -> Optional[Goal]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE goals SET status = 'completed' WHERE id = ? AND user_id = ?",
        (goal_id, user_id)
    )

    if cursor.rowcount > 0:
        connection.commit()
        connection.close()
        return get_goal_by_id(goal_id, user_id)
    else:
        connection.close()
        return None