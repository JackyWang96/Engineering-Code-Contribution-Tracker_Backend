from django.db import models


# Create your models here.


class StudentCommitCounts(models.Model):

    student_name = models.CharField(max_length=256, null=False)
    relation_id = models.CharField(max_length=256, null=True)
    commit_counts = models.CharField(max_length=256, null=False)
    space_key = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = 'student_commit_counts'


class GitContribution(models.Model):

    git_username = models.CharField(max_length=256, null=False)
    username = models.CharField(max_length=256, null=False)
    commit = models.IntegerField(null=False)
    space_key = models.CharField(max_length=256, null=True)
    source = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = 'git_contribution'


class GitCommitCounts(models.Model):
    # student_name = models.CharField(max_length=256, null=False)
    space_key = models.CharField(max_length=256, null=False)
    commit_counts = models.CharField(max_length=256, null=False)
    query_date = models.IntegerField(null=False)

    class Meta:
        db_table = 'git_commit_counts'


class GitMetrics(models.Model):
    space_key = models.CharField(max_length=256, null=False)
    source = models.CharField(max_length=256, null=False)
    CountDeclClass = models.IntegerField(null=False)
    CountDeclExecutableUnit = models.IntegerField(null=False)
    CountDeclFunction = models.IntegerField(null=False)
    CountDeclMethod = models.IntegerField(null=False)
    CountDeclMethodAll = models.IntegerField(null=False)
    CountLine = models.IntegerField(null=False)
    CountDeclFile = models.IntegerField(null=False)
    CountLineBlank = models.IntegerField(null=False)
    CountLineCode = models.IntegerField(null=False)
    CountLineCodeDecl = models.IntegerField(null=False)
    CountLineCodeExe = models.IntegerField(null=False)
    CountLineComment = models.IntegerField(null=False)
    CountPath = models.IntegerField(null=False)
    CountStmt = models.IntegerField(null=False)
    CountStmtDecl = models.IntegerField(null=False)
    CountStmtExe = models.IntegerField(null=False)
    Cyclomatic = models.IntegerField(null=False)
    Essential = models.IntegerField(null=False)
    MaxNesting = models.IntegerField(null=False)
    RatioCommentToCode = models.FloatField(null=False)

    class Meta:
        db_table = 'git_metrics'


class FileMetrics(models.Model):
    space_key = models.CharField(max_length=256, null=False)
    source = models.CharField(max_length=256, null=False)
    file_name = models.CharField(max_length=256, null=False)
    CountDeclClass = models.IntegerField(null=False)
    CountDeclFunction = models.IntegerField(null=False)
    CountDeclExecutableUnit = models.IntegerField(null=False)
    CountLine = models.IntegerField(null=False)
    CountLineBlank = models.IntegerField(null=False)
    CountLineCode = models.IntegerField(null=False)
    CountLineCodeDecl = models.IntegerField(null=False)
    CountLineCodeExe = models.IntegerField(null=False)
    CountLineComment = models.IntegerField(null=False)
    CountPath = models.IntegerField(null=False)
    CountStmt = models.IntegerField(null=False)
    CountStmtDecl = models.IntegerField(null=False)
    CountStmtExe = models.IntegerField(null=False)
    Cyclomatic = models.IntegerField(null=False)
    Essential = models.IntegerField(null=False)
    MaxNesting = models.IntegerField(null=False)
    RatioCommentToCode = models.FloatField(null=False)

    class Meta:
        db_table = 'file_metrics'


class GitCommit(models.Model):
    sha = models.CharField(max_length=256, null=False)
    url = models.CharField(max_length=256, null=False)
    username = models.CharField(max_length=256, null=False)
    date = models.CharField(max_length=256, null=False)
    message = models.CharField(max_length=512, null=False)
    space_key = models.CharField(max_length=256, null=False)
    source = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = 'git_commit'


class GitLastCommit(models.Model):
    url = models.CharField(max_length=256, null=False)
    username = models.CharField(max_length=256, null=False)
    date = models.CharField(max_length=256, null=False)
    message = models.CharField(max_length=512, null=False)
    space_key = models.CharField(max_length=256, null=False)
    source = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = 'git_last_commit'
