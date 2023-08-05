# Generated by Django 4.0 on 2021-12-09 09:51

import django.contrib.postgres.indexes
from django.db import migrations, connection


class Migration(migrations.Migration):

    dependencies = [("core", "0016_auto_20211128_1900")]

    operations = (
        [
            migrations.AddIndex(
                model_name="archivedquery",
                index=django.contrib.postgres.indexes.GinIndex(
                    django.contrib.postgres.indexes.OpClass("query", "gin_trgm_ops"),
                    name="core_archivedquery_query_trgm",
                ),
            ),
            migrations.AddIndex(
                model_name="archivedsong",
                index=django.contrib.postgres.indexes.GinIndex(
                    django.contrib.postgres.indexes.OpClass("artist", "gin_trgm_ops"),
                    name="core_archivedsong_artist_trgm",
                ),
            ),
            migrations.AddIndex(
                model_name="archivedsong",
                index=django.contrib.postgres.indexes.GinIndex(
                    django.contrib.postgres.indexes.OpClass("title", "gin_trgm_ops"),
                    name="core_archivedsong_title_trgm",
                ),
            ),
            # This value was empirically measured on a Raspberry Pi 4
            # so the suggestion query uses the index, as this is the query that runs most often.
            migrations.RunSQL(
                "ALTER DATABASE raveberry SET random_page_cost=1.4;",
                reverse_sql="ALTER DATABASE raveberry RESET random_page_cost;",
            ),
            # Set word_similarity_threshold to the default value of similarity_threshold.
            # With the default value of 0.6 many typos result in no suggestions.
            migrations.RunSQL(
                "ALTER DATABASE raveberry SET pg_trgm.word_similarity_threshold=0.3;",
                # For some reason there is a permission denied error
                # when trying to reset the threshold, even with owner privileges.
                # Simply do nothing, reversing this parameter is not important.
                reverse_sql="",
            ),
        ]
        if connection.vendor == "postgresql"  # trgm is only available in postgres
        else []
    )
