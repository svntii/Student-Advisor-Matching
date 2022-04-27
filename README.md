

<!-- PROJECT LOGO -->

<h3 align="center">Student-Advisor Matching Program</h3>

  <p align="center">
    Santiago Rodriguez, Gabriel Sargent, Eva Gorzkiewicz, Solina Kim
  
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

This program matches students to advisors, using an in-house program based on the Gale-Shapley algorithm. Unlike the Gale-Shapley algorithm, this program does not require equal number of students to advisors, nor does it assume complete cardinal preferences. In other words, it can be used in real life!

For those interested in the Gale-Shapley algorithm, their paper can be found here.
https://www.eecs.harvard.edu/cs286r/courses/fall09/papers/galeshapley.pdf

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Overall, the complete program consists of 3 files: config.py, modules.py, main.py.
config.py contains relevant packages and global variables. In order to adapt the program to your server, manipulate the following variables:

* bot_email_id
  ```
  Complete address of email you wish to use as your program’s server.
  ```
* bot_email_pass
  ```
  Complete password of your program’s email.
  ```
* dir_path
  ```
  Path to your working directory. I/O files will temporarily be saved in this directory, but will be deleted upon completion of program.
  ```
* outf_name
  ```
  Desired name of output file sent to user. Must end with ‘.csv’.
  ```

### Prerequisites

python 3.9


<!-- MODULES -->
## Modules

* receive_email
```
Checks for email with subject line ‘request’ from client, and returns the paths to the downloaded csv files containing advisor and student preferences, adv_csv and stu_csv. Function also returns the client's email address client_email. Note, client’s email is marked as deleted, and will not be found when searched on the gmail browser.
```
* send_email
```
Emails client a the final matches as a csv file.
```
* read_student_pref
```
Parses the pandas dataframe generated from stu_csv and returns a dictionary of student preferences, student_pref.
```
* read_advisor_pref
```
Parses the pandas dataframe generated from adv_csv and returns a dictionary of student preferences, adv_pref.
```
* read_advisor_caps
```
Parses the pandas dataframe generated from adv_csv and returns a dictionary of advisors’ capacities, adv_cap.
```
* generate_results_df
```
Takes in final_list as input and returns a data frame, final_df, with two columns, ‘Advisor’ and ‘Students’.
```
* clean_up
```
Removes all temporary files advisor.csv, student.csv, and match_results.csv from the working directory, dir_path. Should be called after the results are emailed to the client.
```


See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

* Solina Kim - kkim24@nd.edu OR matchmakernd@gmail.com
* Santiago Rodriguez - srodri25@nd.edu

<p align="right">(<a href="#top">back to top</a>)</p>


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png

