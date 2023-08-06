import sys, argparse, logging, os, csv, random
# import funcs
from .employee_scraper import get_all_employee_data, get_employees_from_file
from .download_profile_pics import download_profile_pics
from .company_scraper import extract_company_employees
from .helper_funcs import create_driver, login_through_form, write_genders_to_csv
from .data_storage import Employees
from .gender_detection import detect_genders_from_dir

def run_full_bot() -> None:
    '''
    Runs the full process per the project outlines
    '''
    # create a driver
    driver = create_driver()
    # login
    login_through_form(driver, from_homepage=True)
    # get the list of public profiles
    profiles = extract_company_employees(driver, total_employees=args.tot_employee, return_profiles=True)
    driver.quit()
    # get the employee data from the profile links
    employees = get_all_employee_data(profiles)
    employees.save_as_csv(args.output, max_lines=args.tot_employee)

    # download profile pics
    if not args.no_downloads:
        download_profile_pics(args.output, args.pictures_dir)
        # Face analysis w deepface
        if args.face_detection:
            analysis = detect_genders_from_dir(args.pictures_dir)
            write_genders_to_csv(args.output, analysis)

def main():
    # basic logging settings
    logging.basicConfig(level=logging.INFO if args.debug else logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s', filename=args.log_file if args.debug else None)

    # if no downloads is turned off & pictures dir exists & it's not empty then tell the user to empty it
    if ( not args.no_downloads ) and os.path.isdir(args.pictures_dir) and ( not os.listdir(args.pictures_dir) ):
        print('Please ensure the specified "--pictures-dir" directory is empty.')
        sys.exit(1)

    match args.type:
        case 'hubspot':
            # get the list of public profiles
            # print('getting company info...')
            # run the full thing
            run_full_bot()
        case 'employee':
            # get the info for each profile
            if args.file:
                get_employees_from_file(args.file, output=args.output)
                # download their profile pics
                if not args.no_downloads:
                    download_profile_pics(args.output, args.pictures_dir)
                    if args.face_detection:
                        genders = detect_genders_from_dir(args.pictures_dir)
                        write_genders_to_csv(args.output, genders)
            elif args.profile_link:
                driver = create_driver(headless=True)
                login_through_form(driver, from_homepage=True)
                employees = get_all_employee_data([args.profile_link])
                output = f'\n\n{employees[0].first_name} {employees[0].last_name} ({employees[0].location}) :: {employees[0].label}'
                if not args.no_downloads:
                    download_profile_pics(args.output, args.pictures_dir)
                    if args.face_detection:
                        genders = detect_genders_from_dir(args.pictures_dir)
                        output += f'gender :: {genders.get(1, "unkown")}'
                    output += f'\nphoto storage :: {args.pictures_dir}/'
                print(output + '\n\n')
                return
            else:
                print('Please specify either a file or a profile link.')
                sys.exit(1)
    goodbye = f'Thanks for using leegs.\n{"="*40}\n\ntotal employees :: {len(open(args.output).readlines())-1}\noutput file :: {args.output}'
    if not args.no_downloads:
        goodbye += f'\npictures dir :: {args.pictures_dir}'
        if args.face_detection:
            with open(args.output, 'r') as f:
                reader = csv.reader(f)
                next(reader) # skip first line
                m, f, unkown = 0, 0, 0
                for employee in reader:
                    if employee[-1] == 'Man': m += 1
                    elif employee[-1] == 'Woman': f += 1
                    else: unkown += 1
            goodbye += f'\nface detection :: {m} men | {f} women | {unkown} unkown'
    print(f'{goodbye}\n\n{"="*40}')

if __name__ == '__main__':
    main()

'''CLI ARGUMENTS'''
# set up an argument parser that will parse the command line arguments
parser = argparse.ArgumentParser(description='Scrape LinkedIn for employee data.', formatter_class=argparse.RawTextHelpFormatter)
# basic arguments
parser.add_argument('type', choices=['hubspot', 'employee'], help='''Hubspot // go through hubspot's LinkedIn, extract public employee profiles, then scrape info on each employee
\nEmployee // Scrape employee data for a single profile or a list of profiles''')
parser.add_argument('-o', '--output', type=str, default='data.csv', metavar='', help='filename to save the scraped data')
## download pics argument thats default true and can be turned off
parser.add_argument('-n', '--no-downloads', action='store_true', help='download profile pics')
parser.add_argument('-p', '--pictures-dir', type=str, default=f'profile_pics{random.randint(1,999)}', metavar='', help='directory to save profile pics (required unless you set --no-downloads)')
parser.add_argument('-a', '--face-detection', action='store_true', help='analyze faces of downloaded profile pics')
parser.add_argument('--debug', action='store_true', help='enable logging', default=False)
parser.add_argument('--log-file', type=str, default='log.txt', metavar='', help='filename to save the log')
# args specific to the company scraper
company_args = parser.add_argument_group('company options')
company_args.add_argument('-t', '--tot-employee', type=int, default=100, metavar='', help='total number of employees to scrape')
# args specific to the employee scraper
employee_args = parser.add_argument_group('employee options')
employee_args.add_argument('-f', '--file', type=str, default=None, metavar='', help='file containing the list of profiles to scrape')
employee_args.add_argument('-l', '--profile-link', type=str, default=None, metavar='', help='profile link to scrape')
# args specific to the profile pic
args = parser.parse_args()