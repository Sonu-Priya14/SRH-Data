import csv
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.srh-hochschule-heidelberg.de'

bachelors_links = ['https://www.srh-hochschule-heidelberg.de/en/bachelor/business-engineering/',
                   'https://www.srh-hochschule-heidelberg.de/en/bachelor/study-international-business/international-business/',
                   'https://www.srh-hochschule-heidelberg.de/en/bachelor/study-international-business/international-business/',
                   'https://www.srh-hochschule-heidelberg.de/en/bachelor/electrical-engineering/']


masters_links = ['https://www.srh-hochschule-heidelberg.de/en/master/global-business-and-leadership/',
                'https://www.srh-hochschule-heidelberg.de/en/master/international-management-and-leadership/',
                'https://www.srh-hochschule-heidelberg.de/en/master/information-technology/',
                'https://www.srh-hochschule-heidelberg.de/en/master/international-business-and-engineering/',
                'https://www.srh-hochschule-heidelberg.de/en/master/water-technology/',
                'https://www.srh-hochschule-heidelberg.de/en/master/blockchain-technology/',
                'https://www.srh-hochschule-heidelberg.de/en/master/artificial-intelligence/',
                'https://www.srh-hochschule-heidelberg.de/en/master/architecture/',
                'https://www.srh-hochschule-heidelberg.de/en/master/applied-computer-science/',
                'https://www.srh-hochschule-heidelberg.de/en/master/applied-data-science-and-analytics/',
                'https://www.srh-hochschule-heidelberg.de/en/master/music-therapy/',
                'https://www.srh-hochschule-heidelberg.de/en/master/dance-movement-therapy/']


class SrhFetch:
    def __init__(self):

        self.role = None
        self.professor = None
        self.image_link = None
        self.professor_business_card = None
        self.course_content = None
        self.career_prospects = None
        self.base_url = None
        self.admission_requirements = None
        self.fees_and_funding = None
        self.registration = None
        self.professor_info = None
        self.contact = None
        self.master_degree = None
        self.prof_to_contact = None
        self.course_name = None
        self.all_similar_programmes = {}
        self.semester = None
        self.time = None
        self.ECTS = None
        self.optional_study_abroad = False
        self.intakes = 'Winter and Summer Semester'
        self.all_master_tags = None

        self.base_url = 'https://www.srh-hochschule-heidelberg.de'

    def get_professor_info(self, professor_contact_link):

        professor_contact_link_response = requests.get(professor_contact_link)
        soup1 = BeautifulSoup(professor_contact_link_response.text, 'lxml')
        self.professor_business_card = soup1.find('div', class_='b_rte').p.text
        try:
            table_row_values = soup1.find('div', class_='b_table').find_all('tr')
        except Exception as e:
            print(professor_contact_link)
            print('error ', e)
            self.professor_info = None

        else:
            try:
                self.professor_info = ([each_row.text.strip().replace('\n', ' ') for each_row in table_row_values])
            except:
                print('error finding professor intfo')
            else:
                self.professor_info = None
        try:
            self.image_link = base_url + (soup1.find('picture').img['src'])
        except Exception as e:
            self.image_link = None

    def get_tag_info(self, link):
        # for a_link in all_link:
        # all_similar_programmes, all_similar_programmes, prof_to_contact, contact, registration, fees_and_funding, admission_requirements, career_prospects, course_content = [None] * 9
        # tag, semester, time, ECTS, intakes, optional_study_abroad = [None] * 6

        response1 = requests.get(link)
        soup1 = BeautifulSoup(response1.text, 'lxml')
        self.course_name = soup1.find('h1').text.strip().replace('  ', '')
        print(self.course_name)

        try:
            self.all_master_tags = soup1.find_all('li', class_='b_tag-list__item')
        except Exception as e:
            print(self.all_master_tags, 'tags')
            print(e, link, 'error')
        else:
            self.master_degree = self.all_master_tags[0].text.replace('\n', '')
            print(self.master_degree)

            # #             print(master_degree)
            print([each_tag.text.strip() for each_tag in self.all_master_tags], 'print')
            for tag in [each_tag.text.strip() for each_tag in self.all_master_tags]:
                tag_upper = tag.upper()  # Convert tag to uppercase once for efficiency
                if 'SEMESTERS' in tag_upper:
                    print('inside semesters')
                    self.semester = tag  # Assign the value before the break

                if 'TIME' in tag_upper:
                    self.time = tag
                    print('time')

                if 'ECTS' in tag_upper:
                    print('ECTS')
                    self.ECTS = tag
                if 'ONLY' in tag_upper:
                    self.intakes = tag
                if 'OPTIONAL' in tag_upper:
                    self.optional_study_abroad = True
            print(self.semester, self.time, self.ECTS, self.intakes, self.optional_study_abroad)

    def all_info(self, link):
        # for link in all_link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        all_div = soup.find_all('div', class_='b_container__content-wrap')
        for each_div in all_div:

            try:
                header_value = each_div.header.text.strip()
            except Exception as e:
                print('error', e, link)
            else:
                self.all_similar_programmes = {}
                print(header_value, 'header_value')
                professors_blocks = soup.find_all('article', class_='b_card')
                self.base_url = 'https://www.srh-hochschule-heidelberg.de'
                if header_value == 'Your course content' or header_value == 'YOUR LEARNING CONTENT':
                    self.course_content = each_div.find('div', class_='b_rte').text
                    print(self.course_content, 'self.course_content')
                if header_value == 'Your career prospects':
                    #             if link.split('/')[-1] == 'applied-data-science-and-analytics':
                    #                 print('y')
                    self.career_prospects = ', '.join([_.text for _ in each_div.find('div', 'b_rte').find_all('li')])
                    print(self.career_prospects, 'self.career_prospects')

                if 'Admission requirements' in header_value:
                    self.admission_requirements = each_div.find('div', class_='b_rte').text
                    print(self.admission_requirements, 'self.admission_requirements')
                if 'FEES AND FUNDING' in header_value.upper():
                    self.fees_and_funding = each_div.find('div', class_='b_rte').text
                    print(self.fees_and_funding, 'self.fees_and_funding')
                if 'APPLY NOW' in header_value.upper():
                    self.registration = each_div.find('div', class_='b_rte').text
                    print(self.registration, 'self.registration')
                if 'Your contact' in header_value:
                    self.contact = each_div.find_all('article', class_='b_card')
                    self.prof_to_contact = []
                    for index, professor_block in enumerate(self.contact):
                        role = professor_block.span.text.strip()
                        professor = professor_block.header.text.strip()
                        print(professor)
                        professor_contact_link = base_url + professor_block.a['href']
                        print(professor_contact_link, 'link prof')
                        try:

                            professor_contact_link_response = requests.get(base_url + professor_contact_link)
                        except Exception as e:
                            professor_description = None
                            self.professor_info = None
                            image_link = None
                            print('exeption professor')
                        else:
                            print(professor_contact_link)
                            self.get_professor_info(professor_contact_link)
                        #                 prof_to_contact.append({'role':role,'professor_name':professor})

                        self.prof_to_contact.append(
                            {'role': role, 'professor_name': professor, 'professor_description': professor_description,
                             'professor_info': self.professor_info, 'image_link': image_link})
                    print(self.prof_to_contact)
                #                 print(professor_description, professor_info, image_link)

                if 'Other suitable programmes' in header_value:
                    other_suitable_programme = [_.find('header', class_='b_card__headline').text.strip() for _ in
                                                each_div.find_all('article')]
                    other_suitable_degree = [_.find_all('span', class_='b_card__icon-text')[0].text.strip() for _ in
                                             each_div.find_all('article')]
                    other_suitable_place = [_.find_all('span', class_='b_card__icon-text')[1].text.strip() for _ in
                                            each_div.find_all('article')]
                    for programme, degree, place in zip(other_suitable_programme, other_suitable_degree,
                                                        other_suitable_place):
                        self.all_similar_programmes[programme] = {'degree': degree, 'place': place}

                    print(self.all_similar_programmes)

    def master_save(self):
        with open('./data/masters.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['self.master_degree', 'self.all_similar_programmes', 'self.prof_to_contact',
                 'self.registration', 'self.fees_and_funding', 'self.admission_requirements',
                 'self.career_prospects', 'self.course_content', 'self.semester', 'self.time', 'self.ECTS',
                 'self.intakes', 'self.optional_study_abroad'])

            writer.writerow([self.master_degree, self.all_similar_programmes, self.prof_to_contact,
                             self.registration, self.fees_and_funding, self.admission_requirements,
                             self.career_prospects, self.course_content, self.semester, self.time, self.ECTS,
                             self.intakes, self.optional_study_abroad])
            print([self.master_degree, self.all_similar_programmes, self.prof_to_contact,
                   self.registration, self.fees_and_funding, self.admission_requirements, self.career_prospects,
                   self.course_content,
                   self.semester, self.time, self.ECTS, self.intakes, self.optional_study_abroad])

    def prof_info(self, link,bachelor =False):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')

        professors_blocks = soup.find_all('article', class_='b_card')

        for professor_block in professors_blocks:
            self.role = professor_block.span.text.strip()
            self.professor = professor_block.header.text.strip()
            professor_contact_link = professor_block.a['href']
            try:
                if not bachelor:
                    professor_contact_link_response = requests.get(self.base_url + professor_contact_link)
                else:
                    professor_contact_link_response = requests.get( + professor_contact_link)
            except Exception as e:
                print(f'error as {e}')
            else:
                self.get_professor_info(professor_contact_link)
                # print(proffessor_business_card, professor_info, image_link)

    def bachelors_save(self):
        with open('./data/bachelors.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['self.master_degree', 'self.all_similar_programmes', 'self.prof_to_contact',
                 'self.registration', 'self.fees_and_funding', 'self.admission_requirements',
                 'self.career_prospects', 'self.course_content', 'self.semester', 'self.time', 'self.ECTS',
                 'self.intakes', 'self.optional_study_abroad'])

            writer.writerow([self.master_degree, self.all_similar_programmes, self.prof_to_contact,
                             self.registration, self.fees_and_funding, self.admission_requirements,
                             self.career_prospects, self.course_content, self.semester, self.time, self.ECTS,
                             self.intakes, self.optional_study_abroad])
            print([self.master_degree, self.all_similar_programmes, self.prof_to_contact,
                   self.registration, self.fees_and_funding, self.admission_requirements, self.career_prospects,
                   self.course_content,
                   self.semester, self.time, self.ECTS, self.intakes, self.optional_study_abroad])


srh = SrhFetch()
# for _ in masters_links:
#     srh.get_tag_info(_)
#     srh.all_info(_)
#     srh.master_save()

# for _ in bachelors_links:
#     srh.get_tag_info('https://www.srh-hochschule-heidelberg.de/en/bachelor/electrical-engineering/')
#     srh.all_info('https://www.srh-hochschule-heidelberg.de/en/bachelor/electrical-engineering/')
#     srh.bachelors_save()


# with open('./data/prof.csv', 'a', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['professor', 'role', 'proffessor_business_card', 'professor_info', 'prof_image_link'])
#     for _ in bachelors_links:
#         print(_)
#         # break
#         srh.get_professor_info(_)
#         writer.writerow([srh.professor, srh.role, srh.professor_business_card, srh.professor_info, srh.image_link])
#         print([srh.professor, srh.role, srh.professor_business_card, srh.professor_info, srh.image_link])
#     for _ in masters_links:
#         srh.prof_info(_)
#         writer.writerow([srh.professor, srh.role, srh.professor_business_card, srh.professor_info, srh.image_link])
#         print([srh.professor, srh.role, srh.professor_business_card, srh.professor_info, srh.image_link])

import pandas as pd

pd.set_option('display.max_rows', None)  # None means unlimited
pd.set_option('display.max_columns', None)  # None means unlimited

print(pd.read_csv('bachelors.csv').head())
