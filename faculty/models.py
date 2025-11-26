from django.db import models

# Create your models here.
class Faculty(models.Model):
    # 1. Name: A simple text field for the full name.
    name = models.CharField(
        max_length=100,
        verbose_name='Full Name'
    )

    # 2. Mail ID: Uses Django's specific EmailField and ensures no two faculty members share the same email.
    mail_id = models.EmailField(
        max_length=254,
        unique=True,  # Crucial: Ensures this email is unique in the database
        verbose_name='Email Address'
    )

    # 3. Designation: A simple text field to hold the full designation (e.g., 'Assistant Professor', 'HOD').
    designation = models.CharField(
        max_length=70, 
        verbose_name='Designation'
    )

    # 4. Qualification: A simple text field for the highest qualification.
    qualification = models.CharField(
        max_length=255,
        verbose_name='Highest Qualification'
    )

    # 5. Experience: An integer field to store the years of experience.
    experience = models.IntegerField(
        default=0,
        verbose_name='Years of Experience'
    )
    gender = models.CharField(
        max_length=6,
        verbose_name='Gender'
    )
    # String representation for the Django Admin and debugging.
    def __str__(self):
        return f'{self.name} - {self.mail_id}'
    
    verified = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Faculty"
        ordering = ['name']


class ClassDetails(models.Model):
    # --- Define Choices ---
    
    YEAR_CHOICES = [
        ('puc1', 'PUC 1'),
        ('puc2', 'PUC 2'),
        ('e1', 'E1'),
        ('e2', 'E2'),
        ('e3', 'E3'),
        ('e4', 'E4'),
    ]

    SEM_CHOICES = [
        ('sem1', 'Semester 1'),
        ('sem2', 'Semester 2'),
    ]

    # 1. Year (Using defined choices)
    year = models.CharField(
        max_length=4,  # Max length of the code ('puc1', 'e4')
        choices=YEAR_CHOICES,
        verbose_name='Academic Year'
    )

    # 2. Semester (Using defined choices)
    sem = models.CharField(
        max_length=4,  # Max length of the code ('sem1', 'sem2')
        choices=SEM_CHOICES,
        verbose_name='Semester'
    )

    # 3. Class/Section (e.g., cse1, ece1)
    class_name = models.CharField(
        max_length=20,
        verbose_name='Class/Section Name'
    )
    
    # 4. Faculty Gmail (Foreign Key)
    # Links to the Faculty model using the mail_id field.
    faculty = models.ForeignKey(
        'Faculty', 
        on_delete=models.CASCADE, 
        to_field='mail_id',       
        verbose_name='Faculty In-Charge'
    )

    def __str__(self):
        # Displays the full description for readability
        year_display = dict(self.YEAR_CHOICES).get(self.year, self.year)
        sem_display = dict(self.SEM_CHOICES).get(self.sem, self.sem)
        return f"{year_display} - {sem_display} | {self.class_name}"