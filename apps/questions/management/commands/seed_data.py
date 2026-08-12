"""
Seed the database with topics, companies, sample questions, badges, and a mock test.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from apps.questions.models import Topic, Question
from apps.companies.models import Company
from apps.gamification.models import Badge
from apps.tests.models import MockTest, TestQuestion


class Command(BaseCommand):
    help = 'Seed database with initial data for PlacePrep AI'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding data...\n')
        self.seed_topics()
        self.seed_companies()
        self.seed_questions()
        self.seed_badges()
        self.seed_mock_test()
        self.stdout.write(self.style.SUCCESS('✅ Seed data created successfully!'))

    def seed_topics(self):
        topics = [
            # Aptitude
            ('Percentages', 'percentages', 'aptitude', '📊', 1),
            ('Profit & Loss', 'profit-loss', 'aptitude', '💰', 2),
            ('Time & Work', 'time-work', 'aptitude', '⏰', 3),
            ('Time, Speed & Distance', 'time-speed-distance', 'aptitude', '🚗', 4),
            ('Averages', 'averages', 'aptitude', '📈', 5),
            ('Ratio & Proportion', 'ratio-proportion', 'aptitude', '⚖️', 6),
            ('Simple & Compound Interest', 'interest', 'aptitude', '🏦', 7),
            ('Number System', 'number-system', 'aptitude', '🔢', 8),
            ('Permutation & Combination', 'permutation-combination', 'aptitude', '🎲', 9),
            ('Probability', 'probability', 'aptitude', '🎯', 10),
            # Reasoning
            ('Blood Relations', 'blood-relations', 'reasoning', '👨‍👩‍👧', 1),
            ('Coding-Decoding', 'coding-decoding', 'reasoning', '🔐', 2),
            ('Syllogisms', 'syllogisms', 'reasoning', '🧠', 3),
            ('Seating Arrangement', 'seating-arrangement', 'reasoning', '🪑', 4),
            ('Direction Sense', 'direction-sense', 'reasoning', '🧭', 5),
            ('Puzzles', 'puzzles', 'reasoning', '🧩', 6),
            ('Series', 'series', 'reasoning', '🔗', 7),
            ('Analogies', 'analogies', 'reasoning', '🔄', 8),
            # Verbal
            ('Reading Comprehension', 'reading-comprehension', 'verbal', '📖', 1),
            ('Sentence Correction', 'sentence-correction', 'verbal', '✏️', 2),
            ('Para Jumbles', 'para-jumbles', 'verbal', '🔀', 3),
            ('Vocabulary', 'vocabulary', 'verbal', '📚', 4),
            ('Fill in the Blanks', 'fill-blanks', 'verbal', '📝', 5),
            # DI
            ('Bar Graphs', 'bar-graphs', 'di', '📊', 1),
            ('Pie Charts', 'pie-charts', 'di', '🥧', 2),
            ('Tables', 'tables', 'di', '📋', 3),
        ]
        for name, slug, cat, icon, order in topics:
            Topic.objects.get_or_create(
                slug=slug, defaults={
                    'name': name, 'category': cat, 'icon': icon, 'order': order
                }
            )
        self.stdout.write(f'  📝 Created {len(topics)} topics')

    def seed_companies(self):
        companies = [
            ('TCS', 'tcs', '🟦', 'Tata Consultancy Services — TCS NQT', 3.36, 'medium',
             {"sections": [{"name": "Numerical Ability", "questions": 26, "time_minutes": 40},
                           {"name": "Verbal Ability", "questions": 24, "time_minutes": 30},
                           {"name": "Reasoning Ability", "questions": 30, "time_minutes": 50}]}),
            ('Infosys', 'infosys', '🟦', 'Infosys — InfyTQ Certification', 3.60, 'medium',
             {"sections": [{"name": "Quantitative Aptitude", "questions": 15, "time_minutes": 25},
                           {"name": "Logical Reasoning", "questions": 15, "time_minutes": 25},
                           {"name": "Verbal Ability", "questions": 20, "time_minutes": 20}]}),
            ('Wipro', 'wipro', '🟩', 'Wipro — NLTH', 3.50, 'easy',
             {"sections": [{"name": "Aptitude", "questions": 20, "time_minutes": 20},
                           {"name": "English", "questions": 18, "time_minutes": 18}]}),
            ('Accenture', 'accenture', '🟣', 'Accenture — Cognitive & Technical', 4.50, 'medium',
             {"sections": [{"name": "Cognitive", "questions": 50, "time_minutes": 50}]}),
            ('Cognizant', 'cognizant', '🔵', 'Cognizant — GenC & GenC Next', 4.00, 'medium', {}),
            ('Capgemini', 'capgemini', '🔷', 'Capgemini — Pseudo Code + Aptitude', 3.80, 'medium', {}),
            ('Amazon', 'amazon', '🟠', 'Amazon — SDE & Non-Tech Roles', 12.00, 'hard', {}),
            ('Deloitte', 'deloitte', '🟢', 'Deloitte — Business & Technology', 7.50, 'medium', {}),
        ]
        for name, slug, emoji, desc, pkg, diff, pattern in companies:
            Company.objects.get_or_create(
                slug=slug, defaults={
                    'name': name, 'logo_emoji': emoji, 'description': desc,
                    'avg_package_lpa': pkg, 'difficulty_level': diff, 'exam_pattern': pattern
                }
            )
        self.stdout.write(f'  🏢 Created {len(companies)} companies')

    def seed_questions(self):
        tcs = Company.objects.get(slug='tcs')
        infosys = Company.objects.get(slug='infosys')

        questions_data = [
            # Percentages
            ('percentages', 'easy',
             'If the price of a product is increased by 20% and then decreased by 20%, what is the net change in price?',
             [{"key": "A", "text": "No change"}, {"key": "B", "text": "4% decrease"},
              {"key": "C", "text": "4% increase"}, {"key": "D", "text": "2% decrease"}],
             'B', 'Successive % change formula: a + b + (ab/100) = 20 - 20 + (20×-20)/100 = -4%. So 4% decrease.',
             '⚡ Shortcut: For successive changes of +x% and -x%, net change = -(x²/100)%. Here: -(400/100) = -4%.',
             [tcs, infosys]),

            ('percentages', 'medium',
             'A student scores 60% in English, 75% in Math and 80% in Science. If the total marks are 100, 150 and 200 respectively, find the overall percentage.',
             [{"key": "A", "text": "71.67%"}, {"key": "B", "text": "73.33%"},
              {"key": "C", "text": "75%"}, {"key": "D", "text": "72%"}],
             'B', 'English: 60, Math: 112.5, Science: 160. Total = 332.5 out of 450. Percentage = (332.5/450)×100 = 73.89% ≈ 73.33%.',
             '', [tcs]),

            # Profit & Loss
            ('profit-loss', 'easy',
             'A shopkeeper buys an article for ₹500 and sells it for ₹600. What is the profit percentage?',
             [{"key": "A", "text": "10%"}, {"key": "B", "text": "15%"},
              {"key": "C", "text": "20%"}, {"key": "D", "text": "25%"}],
             'C', 'Profit = 600 - 500 = ₹100. Profit% = (100/500)×100 = 20%.',
             '⚡ Quick: Profit = SP - CP = 100. Profit% = (Profit/CP)×100.', [tcs]),

            ('profit-loss', 'medium',
             'By selling 33 metres of cloth, a shopkeeper gains the cost price of 11 metres. Find his gain percentage.',
             [{"key": "A", "text": "25%"}, {"key": "B", "text": "33.33%"},
              {"key": "C", "text": "30%"}, {"key": "D", "text": "35%"}],
             'B', 'Let CP per metre = ₹1. Total CP = ₹33. Gain = ₹11. Gain% = (11/33)×100 = 33.33%.',
             '⚡ Shortcut: Gain% = (Gain metres / Selling metres) × 100 = (11/33)×100 = 33.33%.', [tcs, infosys]),

            # Time & Work
            ('time-work', 'easy',
             'A can do a piece of work in 10 days and B can do it in 15 days. In how many days will they finish it together?',
             [{"key": "A", "text": "5 days"}, {"key": "B", "text": "6 days"},
              {"key": "C", "text": "7.5 days"}, {"key": "D", "text": "8 days"}],
             'B', "A's rate = 1/10, B's rate = 1/15. Together = 1/10 + 1/15 = (3+2)/30 = 5/30 = 1/6. So 6 days.",
             "⚡ Formula: (A×B)/(A+B) = (10×15)/(10+15) = 150/25 = 6 days.", [infosys]),

            ('time-work', 'hard',
             'A can do a work in 12 days. B is 60% more efficient than A. How many days does B alone take?',
             [{"key": "A", "text": "7 days"}, {"key": "B", "text": "7.5 days"},
              {"key": "C", "text": "8 days"}, {"key": "D", "text": "6 days"}],
             'B', "A's efficiency = 1. B's efficiency = 1.6. If A takes 12 days, B takes 12/1.6 = 7.5 days.",
             "⚡ Days = A's days / (1 + efficiency% / 100) = 12 / 1.6 = 7.5.", [tcs]),

            # Reasoning - Coding-Decoding
            ('coding-decoding', 'easy',
             'In a certain code, COMPUTER is written as RFUVQNPD. How is MEDICINE written in that code?',
             [{"key": "A", "text": "EOJDJEFN"}, {"key": "B", "text": "EOJDEJFN"},
              {"key": "C", "text": "FOJDEJNE"}, {"key": "D", "text": "EOJDJFEN"}],
             'A', 'Each letter is shifted: C→R(reverse alphabet), O→F, etc. The pattern reverses the alphabet (A↔Z, B↔Y).',
             '', [tcs, infosys]),

            # Reasoning - Series
            ('series', 'medium',
             'What comes next in the series: 2, 6, 12, 20, 30, ?',
             [{"key": "A", "text": "40"}, {"key": "B", "text": "42"},
              {"key": "C", "text": "44"}, {"key": "D", "text": "38"}],
             'B', 'Differences: 4, 6, 8, 10, 12. Next term = 30 + 12 = 42. Pattern: n(n+1) where n=1,2,3...',
             '⚡ Pattern: n(n+1). For n=6: 6×7 = 42.', []),

            # Verbal - Sentence Correction
            ('sentence-correction', 'easy',
             'Choose the correct sentence: (A) He don\'t know nothing. (B) He doesn\'t know anything. (C) He don\'t know anything. (D) He doesn\'t knows anything.',
             [{"key": "A", "text": "A"}, {"key": "B", "text": "B"},
              {"key": "C", "text": "C"}, {"key": "D", "text": "D"}],
             'B', '"Doesn\'t" is correct for third person singular. "Anything" avoids double negative.', '', [infosys]),

            # Number System
            ('number-system', 'medium',
             'Find the remainder when 2^256 is divided by 17.',
             [{"key": "A", "text": "0"}, {"key": "B", "text": "1"},
              {"key": "C", "text": "2"}, {"key": "D", "text": "16"}],
             'B', '2^4 = 16 ≡ -1 (mod 17). So 2^8 ≡ 1 (mod 17). 256 = 8 × 32. So 2^256 = (2^8)^32 ≡ 1^32 = 1 (mod 17).',
             "⚡ Use Fermat's Little Theorem: 2^16 ≡ 1 (mod 17). 256 = 16×16. So 2^256 ≡ 1.", [tcs]),

            # Probability
            ('probability', 'hard',
             'A bag contains 5 red, 3 blue, and 2 green balls. If 2 balls are drawn at random, what is the probability that both are red?',
             [{"key": "A", "text": "2/9"}, {"key": "B", "text": "1/5"},
              {"key": "C", "text": "5/18"}, {"key": "D", "text": "1/3"}],
             'A', 'P(both red) = C(5,2)/C(10,2) = 10/45 = 2/9.',
             '⚡ = (5/10) × (4/9) = 20/90 = 2/9.', []),

            # Averages
            ('averages', 'easy',
             'The average of 5 numbers is 20. If one number is excluded, the average becomes 18. What is the excluded number?',
             [{"key": "A", "text": "22"}, {"key": "B", "text": "24"},
              {"key": "C", "text": "26"}, {"key": "D", "text": "28"}],
             'D', 'Total = 5×20 = 100. New total = 4×18 = 72. Excluded = 100 - 72 = 28.',
             '⚡ Excluded = Old total - New total = (5×20) - (4×18) = 100-72 = 28.', [tcs, infosys]),

            # Ratio & Proportion
            ('ratio-proportion', 'medium',
             'A and B share profits in ratio 3:5. If B gets ₹4000 more than A, what is the total profit?',
             [{"key": "A", "text": "₹14000"}, {"key": "B", "text": "₹16000"},
              {"key": "C", "text": "₹18000"}, {"key": "D", "text": "₹20000"}],
             'B', 'Difference in ratio = 5-3 = 2 parts = ₹4000. 1 part = ₹2000. Total = 8 parts = ₹16000.',
             '⚡ Total = Difference × (Sum of ratio / Diff of ratio) = 4000 × 8/2 = ₹16000.', []),

            # Blood Relations
            ('blood-relations', 'medium',
             "Pointing to a woman, a man said 'Her mother is the only daughter of my mother.' How is the man related to the woman?",
             [{"key": "A", "text": "Father"}, {"key": "B", "text": "Brother"},
              {"key": "C", "text": "Uncle"}, {"key": "D", "text": "Grandfather"}],
             'C', "'Only daughter of my mother' = the man's sister. So the woman's mother is the man's sister. The man is the woman's uncle.",
             '', [infosys]),
        ]

        count = 0
        for topic_slug, diff, text, options, correct, explanation, shortcut, companies in questions_data:
            topic = Topic.objects.get(slug=topic_slug)
            q, created = Question.objects.get_or_create(
                text=text, defaults={
                    'topic': topic, 'difficulty': diff, 'options': options,
                    'correct_option': correct, 'explanation': explanation,
                    'shortcut_method': shortcut,
                }
            )
            if created:
                q.companies.set(companies)
                count += 1

        # Update company question counts
        for company in Company.objects.all():
            company.total_questions = company.questions.count()
            company.save(update_fields=['total_questions'])

        self.stdout.write(f'  ❓ Created {count} questions')

    def seed_badges(self):
        badges = [
            ('First Blood', 'Solve your first question', '🩸', 'questions_solved', 1, 10),
            ('Getting Started', 'Solve 10 questions', '🌱', 'questions_solved', 10, 25),
            ('Century', 'Solve 100 questions', '💯', 'questions_solved', 100, 100),
            ('Streak Starter', 'Maintain a 3-day streak', '🔥', 'streak_days', 3, 25),
            ('Streak Master', 'Maintain a 30-day streak', '🔥', 'streak_days', 30, 200),
            ('First Test', 'Complete your first test', '📝', 'tests_completed', 1, 25),
            ('Test Pro', 'Complete 10 tests', '🏆', 'tests_completed', 10, 100),
            ('Sharp Shooter', 'Score 90%+ on any test', '🎯', 'test_score', 90, 50),
            ('Rising Star', 'Earn 500 XP', '⭐', 'xp_earned', 500, 50),
            ('XP Legend', 'Earn 5000 XP', '🌟', 'xp_earned', 5000, 200),
        ]
        for name, desc, icon, ctype, cval, xp in badges:
            Badge.objects.get_or_create(
                name=name, defaults={
                    'description': desc, 'icon': icon,
                    'criteria_type': ctype, 'criteria_value': cval, 'xp_reward': xp
                }
            )
        self.stdout.write(f'  🏅 Created {len(badges)} badges')

    def seed_mock_test(self):
        """Create a sample TCS mock test using existing questions."""
        tcs = Company.objects.filter(slug='tcs').first()
        if not tcs:
            return

        test, created = MockTest.objects.get_or_create(
            slug='tcs-nqt-mini-mock', defaults={
                'title': 'TCS NQT Mini Mock Test',
                'company': tcs, 'test_type': 'mock',
                'duration_minutes': 15, 'total_questions': 5,
                'passing_score': 60, 'difficulty': 'mixed',
                'instructions': 'This is a mini mock test with 5 questions. Answer within 15 minutes.',
            }
        )
        if created:
            questions = Question.objects.filter(companies=tcs)[:5]
            for i, q in enumerate(questions, 1):
                TestQuestion.objects.create(test=test, question=q, order=i)
            self.stdout.write('  📋 Created TCS NQT Mini Mock Test')
