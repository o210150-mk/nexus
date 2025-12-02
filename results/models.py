import datetime
from django.db import models
from student.models import Student

class SubjectInfo(models.Model):
    # Subject code (e.g., 'CS101', 'MATH305')
    # This is set as the primary key.
    subject_code = models.CharField(
        max_length=15, 
        primary_key=True, 
        # Help text for clarity in the admin interface
        help_text="The unique code for the subject (e.g., CS101)."
    )
    
    # Name of the subject (e.g., 'Introduction to Computer Science')
    name = models.CharField(
        max_length=100,
        help_text="The full name of the subject."
    )
    
    # Credits of the subject (Assuming an integer value like 3 or 4)
    credits = models.IntegerField(
        help_text="The credit weight for the subject."
    )

    year = models.CharField(
        max_length=5,
        help_text="The full name of the subject."
    )

    # Optional: Define a human-readable representation for the object
    def __str__(self):
        return f"{self.subject_code}: {self.name}"
    
class ResultE1S1(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E1-SEM1"
        ordering = ['student', 'subject', 'year_of_pass']
    

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"
    
class ResultE1S2(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E1-SEM2"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"
    
class ResultE2S1(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E2-SEM1"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultE2S2(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E2-SEM2"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"
    
class ResultE3S1(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E3-SEM1"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultE3S2(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E3-SEM2"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultE4S1(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E4-SEM1"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultE4S2(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "E4-SEM2"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultP1S1(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "PUC1-SEM1"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultP1S2(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "PUC1-SEM2"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultP2S1(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "PUC2-SEM1"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"

class ResultP2S2(models.Model):
    # Foreign Key to the Student table
    # 'on_delete=models.CASCADE' means if a Student is deleted, their enrollment records are also deleted.
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'idno'
        db_column='idNo', 
        help_text="The ID number of the student."
    )
    
    # Foreign Key to the Subject table
    # This links the enrollment record to the specific subject taken.
    subject = models.ForeignKey(
        'SubjectInfo', 
        on_delete=models.CASCADE,
        # The column name in the database will be 'subject_code'
        db_column='subject_code', 
        help_text="The code of the subject."
    )

    # Midterm Examination Marks (Assuming marks are out of 100 or another integer value)
    mid1 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 1.")
    mid2 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 2.")
    mid3 = models.IntegerField(null=True, blank=True, help_text="Marks secured in Midterm 3.")
    
    WAT = models.IntegerField(null=True, blank=True, help_text="Marks secured in WAT.")

    # Grade received (e.g., 'A', 'B+', 'F')
    grade = models.CharField(max_length=2, null=True, blank=True, help_text="Final grade received for the subject.")
    
    # Year the student passed the subject
    year_of_pass = models.CharField(null=True, blank=True, help_text=" MMYY ; ex - 0125 : january 2025", max_length=4)

    bulk = models.DateField(default = datetime.date.today)

    # Optional: Define a composite primary key or unique constraint
    class Meta:
        # Ensures that a student can only have ONE enrollment record per subject
        unique_together = ('student', 'subject', 'year_of_pass') 
        verbose_name_plural = "PUC2-SEM2"
        ordering = ['student', 'subject', 'year_of_pass']

    def __str__(self):
        return f"Enrollment for {self.student.idNo} in {self.subject.subject_code}"