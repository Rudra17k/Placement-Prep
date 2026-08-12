"""
Bulk import questions from a CSV file.

CSV Format:
topic_slug,difficulty,text,option_a,option_b,option_c,option_d,correct_option,explanation,shortcut_method,company_slugs

Example CSV row:
percentages,easy,"If 20% of X is 40, what is X?",100,150,200,250,C,"20% of X = 40. X = 40 × 100/20 = 200","Shortcut: X = Value × 100/Percentage","tcs,infosys"

Usage:
    python manage.py import_questions path/to/questions.csv
"""
import csv
from django.core.management.base import BaseCommand
from apps.questions.models import Topic, Question
from apps.companies.models import Company


class Command(BaseCommand):
    help = 'Import questions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Preview import without saving to database'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        dry_run = options['dry_run']
        created = 0
        skipped = 0
        errors = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate topic
                        topic_slug = row.get('topic_slug', '').strip()
                        try:
                            topic = Topic.objects.get(slug=topic_slug)
                        except Topic.DoesNotExist:
                            errors.append(f"Row {row_num}: Topic '{topic_slug}' not found")
                            continue

                        # Validate difficulty
                        difficulty = row.get('difficulty', 'medium').strip().lower()
                        if difficulty not in ('easy', 'medium', 'hard'):
                            errors.append(f"Row {row_num}: Invalid difficulty '{difficulty}'")
                            continue

                        # Build options
                        options_list = [
                            {"key": "A", "text": row.get('option_a', '').strip()},
                            {"key": "B", "text": row.get('option_b', '').strip()},
                            {"key": "C", "text": row.get('option_c', '').strip()},
                            {"key": "D", "text": row.get('option_d', '').strip()},
                        ]

                        correct = row.get('correct_option', '').strip().upper()
                        if correct not in ('A', 'B', 'C', 'D'):
                            errors.append(f"Row {row_num}: Invalid correct_option '{correct}'")
                            continue

                        text = row.get('text', '').strip()
                        if not text:
                            errors.append(f"Row {row_num}: Empty question text")
                            continue

                        # Check for duplicate
                        if Question.objects.filter(text=text).exists():
                            skipped += 1
                            continue

                        if not dry_run:
                            q = Question.objects.create(
                                topic=topic,
                                difficulty=difficulty,
                                text=text,
                                text_hi=row.get('text_hi', '').strip(),
                                options=options_list,
                                correct_option=correct,
                                explanation=row.get('explanation', '').strip(),
                                shortcut_method=row.get('shortcut_method', '').strip(),
                            )

                            # Tag companies
                            company_slugs = row.get('company_slugs', '').strip()
                            if company_slugs:
                                for slug in company_slugs.split(','):
                                    slug = slug.strip()
                                    try:
                                        company = Company.objects.get(slug=slug)
                                        q.companies.add(company)
                                    except Company.DoesNotExist:
                                        pass

                        created += 1

                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")

        except FileNotFoundError:
            self.stderr.write(f'❌ File not found: {csv_file}')
            return

        # Update company question counts
        if not dry_run:
            for company in Company.objects.all():
                company.total_questions = company.questions.count()
                company.save(update_fields=['total_questions'])

        # Report
        prefix = "[DRY RUN] " if dry_run else ""
        self.stdout.write(f'\n{prefix}📊 Import Summary:')
        self.stdout.write(self.style.SUCCESS(f'  ✅ {created} questions {"would be " if dry_run else ""}created'))
        if skipped:
            self.stdout.write(f'  ⏭️  {skipped} duplicates skipped')
        if errors:
            self.stdout.write(self.style.WARNING(f'  ⚠️  {len(errors)} errors:'))
            for e in errors[:10]:
                self.stdout.write(f'     {e}')
            if len(errors) > 10:
                self.stdout.write(f'     ... and {len(errors) - 10} more')
