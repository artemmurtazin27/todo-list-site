from django.test import TestCase
from django.urls import reverse

from todo.forms import TaskForm
from todo.models import Tag, Task


class TagModelTest(TestCase):
    def test_tag_str_returns_name(self):
        tag = Tag.objects.create(name="Work")
        self.assertEqual(str(tag), "Work")

    def test_tags_are_ordered_by_name(self):
        Tag.objects.create(name="Zebra")
        Tag.objects.create(name="Alpha")
        Tag.objects.create(name="Mango")

        names = list(Tag.objects.values_list("name", flat=True))

        self.assertEqual(names, ["Alpha", "Mango", "Zebra"])


class TaskModelTest(TestCase):
    def test_task_str_returns_content(self):
        task = Task.objects.create(content="Buy milk")
        self.assertEqual(str(task), "Buy milk")

    def test_task_defaults_to_not_completed(self):
        task = Task.objects.create(content="Read a book")
        self.assertFalse(task.completed)

    def test_task_datetime_is_set_automatically(self):
        task = Task.objects.create(content="Write tests")
        self.assertIsNotNone(task.datetime)

    def test_completed_tasks_are_ordered_after_pending_ones(self):
        done = Task.objects.create(content="Done task", completed=True)
        pending = Task.objects.create(content="Pending task", completed=False)

        tasks = list(Task.objects.all())

        self.assertEqual(tasks, [pending, done])

    def test_task_can_have_multiple_tags(self):
        tag_home = Tag.objects.create(name="Home")
        tag_urgent = Tag.objects.create(name="Urgent")
        task = Task.objects.create(content="Clean the house")

        task.tags.add(tag_home, tag_urgent)

        self.assertEqual(task.tags.count(), 2)
        self.assertIn(tag_home, task.tags.all())


class TaskFormTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="General")

    def test_form_is_valid_with_content_and_tag(self):
        form = TaskForm(data={"content": "Water the plants", "tags": [self.tag.pk]})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_without_content(self):
        form = TaskForm(data={"content": "", "tags": [self.tag.pk]})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_form_is_invalid_without_tags(self):
        form = TaskForm(data={"content": "No tags here", "tags": []})
        self.assertFalse(form.is_valid())
        self.assertIn("tags", form.errors)

    def test_form_accepts_datetime_local_format(self):
        form = TaskForm(
            data={
                "content": "Submit report",
                "deadline": "2026-12-31T23:59",
                "tags": [self.tag.pk],
            }
        )
        self.assertTrue(form.is_valid())


class IndexViewTest(TestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse("todo:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/index.html")

    def test_index_lists_existing_tasks(self):
        task = Task.objects.create(content="Existing task")

        response = self.client.get(reverse("todo:index"))

        self.assertContains(response, "Existing task")
        self.assertIn(task, response.context["tasks"])


class ToggleTaskStatusViewTest(TestCase):
    def test_toggle_flips_completed_flag(self):
        task = Task.objects.create(content="Toggle me", completed=False)

        response = self.client.get(reverse("todo:task-toggle", args=[task.pk]))
        task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(task.completed)

    def test_toggle_twice_returns_to_original_state(self):
        task = Task.objects.create(content="Toggle twice", completed=False)

        self.client.get(reverse("todo:task-toggle", args=[task.pk]))
        self.client.get(reverse("todo:task-toggle", args=[task.pk]))
        task.refresh_from_db()

        self.assertFalse(task.completed)

    def test_toggle_missing_task_returns_404(self):
        response = self.client.get(reverse("todo:task-toggle", args=[9999]))
        self.assertEqual(response.status_code, 404)


class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="General")

    def test_get_create_form_returns_200(self):
        response = self.client.get(reverse("todo:task-create"))
        self.assertEqual(response.status_code, 200)

    def test_post_creates_task_and_redirects(self):
        response = self.client.post(
            reverse("todo:task-create"),
            data={"content": "New task from form", "tags": [self.tag.pk]},
        )
        self.assertRedirects(response, reverse("todo:index"))
        self.assertTrue(Task.objects.filter(content="New task from form").exists())


class TaskUpdateViewTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="General")
        self.task = Task.objects.create(content="Old content")
        self.task.tags.add(self.tag)

    def test_post_updates_task(self):
        response = self.client.post(
            reverse("todo:task-update", args=[self.task.pk]),
            data={"content": "Updated content", "tags": [self.tag.pk]},
        )
        self.task.refresh_from_db()

        self.assertRedirects(response, reverse("todo:index"))
        self.assertEqual(self.task.content, "Updated content")


class TaskDeleteViewTest(TestCase):
    def test_post_deletes_task(self):
        task = Task.objects.create(content="Task to delete")

        response = self.client.post(reverse("todo:task-delete", args=[task.pk]))

        self.assertRedirects(response, reverse("todo:index"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())


class TagListViewTest(TestCase):
    def test_tag_list_returns_200_and_shows_tags(self):
        Tag.objects.create(name="Personal")

        response = self.client.get(reverse("todo:tag-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Personal")


class TagCreateViewTest(TestCase):
    def test_post_creates_tag_and_redirects(self):
        response = self.client.post(
            reverse("todo:tag-create"), data={"name": "Shopping"}
        )
        self.assertRedirects(response, reverse("todo:tag-list"))
        self.assertTrue(Tag.objects.filter(name="Shopping").exists())


class TagUpdateViewTest(TestCase):
    def test_post_updates_tag_name(self):
        tag = Tag.objects.create(name="Old name")

        response = self.client.post(
            reverse("todo:tag-update", args=[tag.pk]), data={"name": "New name"}
        )
        tag.refresh_from_db()

        self.assertRedirects(response, reverse("todo:tag-list"))
        self.assertEqual(tag.name, "New name")


class TagDeleteViewTest(TestCase):
    def test_post_deletes_tag(self):
        tag = Tag.objects.create(name="Temporary")

        response = self.client.post(reverse("todo:tag-delete", args=[tag.pk]))

        self.assertRedirects(response, reverse("todo:tag-list"))
        self.assertFalse(Tag.objects.filter(pk=tag.pk).exists())
