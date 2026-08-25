USE research_platform;

SELECT 
    u.user_id,
    u.name,
    u.email,
    u.role,
    f.faculty_id,
    f.department
FROM users u
JOIN faculty f ON u.user_id = f.user_id
WHERE u.role = 'FACULTY';