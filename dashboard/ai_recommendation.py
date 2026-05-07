def recommend_opportunities(user, opportunities):
    recommended = []

    user_major = (user.get("major") or "").lower()
    user_interests = user.get("interests") or ""
    user_skills = user.get("skills") or ""
    user_department = (user.get("department") or "").lower()
    user_location = (user.get("location") or "").lower()

    if isinstance(user_interests, str):
        user_interests = [
            interest.strip().lower()
            for interest in user_interests.split(",")
            if interest.strip()
        ]
    else:
        user_interests = [
            str(interest).lower()
            for interest in user_interests
            if interest
        ]

    if isinstance(user_skills, str):
        user_skills = [
            skill.strip().lower()
            for skill in user_skills.split(",")
            if skill.strip()
        ]
    else:
        user_skills = [
            str(skill).lower()
            for skill in user_skills
            if skill
        ]

    for opp in opportunities:
        title = getattr(opp, "name", "")
        category = getattr(opp, "category", "")
        description = getattr(opp, "description", "")
        location = getattr(opp, "location", "").lower()

        title_lower = str(title).lower()
        category_lower = str(category).lower()
        desc_lower = str(description).lower()

        score = 0

        if user_major and user_major in category_lower:
            score += 3

        if user_department and user_department in category_lower:
            score += 2

        if any(i in category_lower for i in user_interests):
            score += 3

        if any(i in title_lower for i in user_interests):
            score += 2

        if any(i in desc_lower for i in user_interests):
            score += 2

        if any(s in category_lower for s in user_skills):
            score += 3

        if any(s in title_lower for s in user_skills):
            score += 2

        if any(s in desc_lower for s in user_skills):
            score += 2

        if user_major and user_major in title_lower:
            score += 2

        if user_department and user_department in title_lower:
            score += 1

        if location and location in user_department:
            score += 2

        if user_location and user_location in location:
            score += 3

        if score > 0:
            recommended.append({
                "id": opp.id,
                "name": title,
                "category": category,
                "location": getattr(opp, "location", ""),
                "hours": getattr(opp, "hours", ""),
                "score": score
            })

    recommended = sorted(recommended, key=lambda x: x["score"], reverse=True)

    return recommended[:3]