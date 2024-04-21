SELECT * FROM SPECIES;

ALTER TABLE SPECIES
RENAME COLUMN SPECIES ID TO species_id;

SELECT COUNT(*),SPECIES ID FROM SPECIES
GROUP BY SPECIES ID ;

select * from species2;

select * from parks;

ALTER TABLE `biodiversity`.`blackcanyon` 
ADD COLUMN `park_code` CHAR(4) NULL DEFAULT 'BLCA' AFTER `AnnualTotal`;

SELECT park_code_act,activity FROM activities_parks
where activity like '%wildlife%'
group by park_code_act,activity
;


drop column Textbox4 from arches;

ALTER TABLE `biodiversity`.`everglades`
DROP COLUMN `Unnamed: 0`,
DROP COLUMN `Unnamed: 0.1`,
DROP COLUMN `MyUnknownColumn`;

