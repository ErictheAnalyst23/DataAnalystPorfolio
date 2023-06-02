/* The following queries will explore the dataset published on the website 'Our World in Data' in regards to key statistics about COVID19.
These queries will help summarise information such as the number of deaths, number of cases and vaccinations administered. */

-- Checkpoint 1:
-- Explore the changes in case numbers, deaths, population size for each location.
SELECT location, date, total_cases, new_cases, total_deaths, population
FROM CovidDeaths$
ORDER BY 1,2;


-- Checkpoint 2:
-- To examine the percentage of individuals contracting COVID in Australia.
-- To examine the percentage of case numbers and death count due to COVID.
SELECT location, date, population, total_cases, (total_cases/population)*100 AS CasePercentage,
total_deaths, (total_deaths/total_cases)*100  AS DeathPercentage
FROM CovidDeaths$
WHERE location LIKE 'Australia'
ORDER BY 1,2;



-- Checkpoint 3
-- Explore which country has the highest infection rates for COVID
SELECT location, population, MAX(total_cases) AS HighestInfectionCount, MAX((total_cases/population))*100 AS MaxPercentPopulationInfected
FROM CovidDeaths$
GROUP BY location, population
ORDER BY 4 DESC;

-- Checkpoint 4
-- The following query will show the countries with the highest death count based on their population.
SELECT location, MAX(total_deaths) AS MaxDeathCount
FROM CovidDeaths$
GROUP BY location
ORDER BY 2 DESC;


-- Checkpoint 5
-- Explore the changes in the global numbers of new cases, new deaths and compare it as a percentage.
-- HAVING statement to ensure the aggregation does not have a division by zero error.
SELECT date, SUM(new_cases) AS total_cases, SUM(new_deaths) AS total_deaths, SUM(new_deaths)/SUM(new_cases)*100 AS DeathPercentage
FROM CovidDeaths$
GROUP BY date
HAVING SUM(new_cases) > 0
ORDER BY 1,2;

-- Checkpoint 6
-- Explore the total vaccines administered, including first doses, second doses and booster shots
-- Explore the percentage of people not vaccinated and those who have obtained a booster shot
SELECT location, MAX(total_vaccinations) AS Total_Vaccination_Count, MAX(people_vaccinated) AS Partial_Vaccinated_Count,
MAX(people_fully_vaccinated) AS Fully_Vaccinated_Count, MAX(total_boosters) AS Total_Booster_Count,
(100 - (MAX(people_vaccinated)/MAX(population)*100)) AS Percentage_Not_Vaccinated, 
MAX(total_boosters)/MAX(population)*100 AS Pop_Percent_boosted
FROM CovidVaccinations$
GROUP BY location
ORDER BY 2 DESC;

-- Checkpoint 7
-- GDP Per Capita and Vaccination rate
SELECT location, MAX(people_vaccinated_per_hundred) AS Percentage_people_vaccinated, MAX(gdp_per_capita) AS GDP_per_Capita
FROM CovidVaccinations$
GROUP BY location
ORDER BY 3 DESC;


-- Checkpoint 8
-- Formed an inner join between two tables
-- The following will explore the running total of vaccines administered for each location 
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingTotalVaccinations
FROM CovidDeaths$ AS dea
JOIN CovidVaccinations$ AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE vac.new_vaccinations is not null 
ORDER BY 2,3;

-- Checkpoint 9
-- CTE was made to investigate the rolling percentage change in the vaccinations amongst the population as checkpoint 8
WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingTotalVaccinations)
AS (
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingTotalVaccinations
FROM CovidDeaths$ AS dea
JOIN CovidVaccinations$ AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE vac.new_vaccinations is not null 
)
SELECT *, (RollingTotalVaccinations/population)*100 AS VaccinatedPopulationPercentage
FROM PopvsVac;



-- Checkpoint 10
-- Using a TEMP Table to conduct the PARTITION BY from checkpoint 8
DROP TABLE IF EXISTS #PercentPopulationVaccinated 
CREATE TABLE #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
RollingTotalVaccinations numeric)

INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingTotalVaccinations
FROM CovidDeaths$ AS dea
JOIN CovidVaccinations$ AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE vac.new_vaccinations is not null 

SELECT *, (RollingTotalVaccinations/population)*100 AS VaccinatedPopulationPercentage
FROM #PercentPopulationVaccinated;


--Creating view to store data for later visualisation
CREATE VIEW PercentageOfPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingTotalVaccinations
FROM CovidDeaths$ AS dea
JOIN CovidVaccinations$ AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE vac.new_vaccinations is not null 


/* Query was completed on SQL Server. Information acquired from this investigation was visualised in tableau. 
Link to Tableau Dashboard:
https://public.tableau.com/app/profile/eric.wong8260/viz/CovidVaccinationTracker_16849971901100/Dashboard1

Thank you for reading. */