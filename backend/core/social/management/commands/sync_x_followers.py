from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from core.social.follower_sync import sync_x_followers_snapshot


class Command(BaseCommand):
    help = "Sync X followers snapshot and detect new followers/unfollowers (official API)."

    def add_arguments(self, parser):
        parser.add_argument("--account", required=True, help="SocialAccount UUID")
        parser.add_argument("--max-pages", type=int, default=50)
        parser.add_argument("--page-size", type=int, default=1000)

    def handle(self, *args, **options):
        account_id = options["account"]
        try:
            result = sync_x_followers_snapshot(
                social_account_id=account_id,
                max_pages=options["max_pages"],
                page_size=options["page_size"],
            )
        except Exception as exc:
            raise CommandError(str(exc))

        self.stdout.write(
            self.style.SUCCESS(
                f"X follower sync ok: account={result.account_id} fetched={result.fetched_users} new={result.new_followers} unfollow={result.unfollowers}"
            )
        )
