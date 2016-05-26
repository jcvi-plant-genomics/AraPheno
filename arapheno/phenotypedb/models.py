from __future__ import unicode_literals

from django.db import models

'''
Species Model
'''
class Species(models.Model):
    ncbi_id = models.IntegerField(blank=True,null=True) #NCBI Taxonomy ID
    genus = models.CharField(max_length=255)  #Genus, e.g. Arabidopsis
    species = models.CharField(max_length=255) #Species, e.g. thaliana
    species_description = models.TextField(blank=True,null=True) #short species description


'''
Study Model
each phenotype is grouped into a study and a study is linked to a certain phenotype
'''
class Study(models.Model):
    study_name = models.CharField(max_length=255) #name of study/experiment
    study_description = models.TextField(blank=True,null=True) #short study description

    species = models.ForeignKey("Species") #foreign key to species
    publications = models.ManyToManyField("Publication",blank=True)


'''
Accession Model
'''
class Accession(models.Model):
    accession_id = models.CharField(db_index=True,max_length=255) #unique accession id
    accession_name = models.CharField(max_length=255,db_index=True,blank=True,null=True) #accession name if available
    accession_description = models.TextField(blank=True,null=True) #short accession description
    
    url = models.TextField(blank=True,null=True) #URL to accession at e.g. 1001genomes.org

    #meta-information fields for accession
    source = models.TextField(blank=True,null=True) #source of accession if available
    country = models.CharField(max_length=255,blank=True,null=True) #country of accession if available
    sitename = models.TextField(blank=True,null=True) #name of site if available
    collector = models.TextField(blank=True,null=True) #collector if available
    collection_date = models.DateTimeField(auto_now_add=True) #date of phenotype integration/submission
    longitude = models.FloatField(null=True,blank=True,db_index=True) #longitude of accession
    latitude = models.FloatField(null=True,blank=True,db_index=True) #latitude of accession

    species = models.ForeignKey("Species") #species foreign key
    publications = models.ManyToManyField("Publication",blank=True)


'''
Phenotype Model
'''
class Phenotype(models.Model):
    phenotype_id = models.CharField(max_length=40,db_index=True) #Unique AraPheno ID
    doi = models.CharField(max_length=255,db_index=True,null=True,blank=True) #DOI for phenotype
    phenotype_name = models.CharField(max_length=255,db_index=True) #phenotype name
    phenotype_scoring = models.TextField(blank=True,null=True) #how was the scoring of the phenotype done
    phenotype_source = models.TextField(blank=True,null=True) #person who colleted the phenotype. or from which website was the phenotype
    phenotype_type = models.CharField(max_length=255,blank=True,null=True) #type/category of the phenotype
    growth_conditions = models.TextField(blank=True,null=True) #description of the growth conditions of the phenotype
    eo_term = models.CharField(max_length=255,db_index=True,blank=True,null=True) # environmental ontology terms from gramene
    to_term = models.CharField(max_length=255,db_index=True,blank=True,null=True) # trait ontology terms from gramene
    hdf5_file = models.CharField(max_length=255,blank=True,null=True) #file to phenotype data
    shapiro_test_statistic = models.FloatField(blank=True,null=True) #Shapiro Wilk test for normality
    shapiro_p_value = models.FloatField(blank=True,null=True) #p-value of Shapiro Wilk test
    number_replicates = models.IntegerField(default=0) #number of replicates for this phenotype
    integration_date = models.DateTimeField(auto_now_add=True) #date of phenotype integration/submission

    species = models.ForeignKey('Species')
    study = models.ForeignKey('Study')
    accessions = models.ManyToManyField('Accession')
    dynamic_metainformations = models.ManyToManyField('PhenotypeMetaDynamic')
    publications = models.ManyToManyField("Publication",blank=True)


'''
Dynamic Phenotype Meta-Information Model
'''
class PhenotypeMetaDynamic(models.Model):
    phenotype_meta_field = models.CharField(db_index=True, max_length=255) #field/key of the meta field
    phenotype_meta_value = models.TextField() #value of the meta information

    phenotype_public = models.ForeignKey('Phenotype',null=True,blank=True)


'''
Authos Model for Publications
'''
class Author(models.Model):
    firstname = models.CharField(max_length=100,blank=True,null=True) #firstname of author
    lastname = models.CharField(max_length=200,blank=True,null=True,db_index=True) #last name of author
    
    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)


'''
Publication Model
'''
class Publication(models.Model):
    author_order = models.TextField() #order of author names
    publication_tag = models.CharField(max_length=255) #publication tag
    pub_year = models.IntegerField(blank=True,null=True) #year of publication
    title = models.CharField(max_length=255, db_index=True) #title of publication
    journal = models.CharField(max_length=255) #journal of puplication
    volume = models.CharField(max_length=255,blank=True,null=True) # volume of publication
    pages = models.CharField(max_length=255,blank=True,null=True) # pages
    doi = models.CharField(max_length=255, db_index=True,blank=True,null=True) #doi
    pubmed_id = models.CharField(max_length=255, db_index=True,blank=True,null=True) #pubmed id
    
    authors = models.ManyToManyField("Author") #author link
